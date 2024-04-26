import os
import matplotlib.pyplot as plt
import matplotlib.backends.backend_pdf
import pandas as pd
from format import adapt_columns
from get_flight_info import get_flight_info
from gui import *
from datetime import date
matplotlib.use('agg')


def get_prices(airport_from, airport_to, date_of_flights, n_of_persons):

    # Specifica il percorso della cartella da creare
    excel_folder = "tabella_prezzi"
    plot_folder = "grafici"

    if not os.path.exists(excel_folder):
        os.makedirs(excel_folder)
    if not os.path.exists(plot_folder):
        os.makedirs(plot_folder)

    sheet_name = airport_from + '-' + airport_to
    excel_file = excel_folder + '/' + n_of_persons + '-' + sheet_name + "-" + ",".join(date_of_flights) + ".xlsx"
    plot_file = excel_file.replace(".xlsx", ".pdf").replace(excel_folder, plot_folder)

    columns_complete_flight, prices = [], []

    for date_of_flight in date_of_flights:
        URL = (f"https://www.ryanair.com/it/it/trip/flights/select?adults={n_of_persons}&teens=0&children=0&infants=0"
               f"&dateOut={date_of_flight}&dateIn=&isConnectedFlight=false&discount=0&promoCode=&isReturn=false"
               f"&originIata={airport_from}&destinationIata={airport_to}&tpAdults={n_of_persons}&tpTeens=0&tpChildren=0&"
               f"tpInfants=0&tpStartDate={date_of_flight}&tpEndDate=&tpDiscount=0&tpPromoCode=&tpOriginIata={airport_from}&"
               f"tpDestinationIata={airport_to}")
        # print(URL)

        info = get_flight_info(URL)

        if info:
            for flight in info:
                columns_complete_flight.append(date_of_flight + ", " + flight['Departure'] + "-" + flight['Arrival'])
                prices.append(flight['Price'])
                # print(flight)

    if os.path.exists(excel_file):
        df = pd.read_excel(excel_file, sheet_name=sheet_name, index_col=0)
    elif columns_complete_flight:
        df = pd.DataFrame(index=["Prezzi al " + str(date.today())], columns=columns_complete_flight)

    if prices and len(prices) == len(columns_complete_flight):
        df.loc["Prezzi al " + str(date.today())] = [float(price.replace(' €', '').replace(',', '.')) for price in prices]
        df.to_excel(excel_file, sheet_name=sheet_name)
        adapt_columns(excel_file, sheet_name)
        # print("\n\n" + df.to_string())

        plot_prices(df, columns_complete_flight)
        plt.savefig(plot_file)
        plt.close()

        try:
            open_file(plot_file)
            open_file(excel_file)
        except FileNotFoundError:
            print("file not found.")


def open_file(file_path):
    if os.name == 'posix':  # macOS e Linux
        os.system('open "{}"'.format(file_path))
    elif os.name == 'nt':  # Windows
        os.system('start "" "{}"'.format(file_path))
    else:
        raise OSError("Sistema operativo non supportato")


def plot_prices(df, columns_complete_flight):
    fig = plt.figure()
    plt.figure(figsize=(10, 8))

    x = df.index.values.tolist()
    y = df.values.tolist()

    plt.xticks(range(len(x)), x)
    plt.plot(y, "-o")
    plt.ylabel("€")
    plt.grid()

    plt.legend(columns_complete_flight, bbox_to_anchor=(0.5, 1.2), loc='upper center', ncol=3)
    plt.tight_layout()

    plt.gcf().autofmt_xdate()


if __name__ == "__main__":
    app = Home()
    app.mainloop()