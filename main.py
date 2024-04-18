from get_flight_info import *
from format import *
from gui import *
from datetime import date
import pandas as pd
import os
import matplotlib.pyplot as plt
import matplotlib.backends.backend_pdf
import keyboard


def get_prices(airport_from, airport_to, date_of_flights, n_of_persons):
    sheet_name = airport_from + '-' + airport_to
    excel_file = sheet_name + "-" + ",".join(date_of_flights) + ".xlsx"

    col, prices = [], []

    for date_of_flight in date_of_flights:
        print("\n\nAnalizzando voli in data " + date_of_flight)
        URL = (f"https://www.ryanair.com/it/it/trip/flights/select?adults={n_of_persons}&teens=0&children=0&infants=0"
               f"&dateOut={date_of_flight}&dateIn=&isConnectedFlight=false&discount=0&promoCode=&isReturn=false"
               f"&originIata={airport_from}&destinationIata={airport_to}&tpAdults={n_of_persons}&tpTeens=0&tpChildren=0&"
               f"tpInfants=0&tpStartDate={date_of_flight}&tpEndDate=&tpDiscount=0&tpPromoCode=&tpOriginIata={airport_from}&"
               f"tpDestinationIata={airport_to}")
        # print(URL)

        info = get_flight_info(URL)

        if info:
            for flight in info:
                col.append(date_of_flight + ", " + flight['Departure'] + "-" + flight['Arrival'])
                prices.append(flight['Price'])
                print(flight)

    if os.path.exists(excel_file):
        df = pd.read_excel(excel_file, sheet_name=sheet_name, index_col=0)
    elif col:
        df = pd.DataFrame(index=["Prezzi al " + str(date.today())], columns=col)

    if prices and len(prices) == len(col):
        df.loc["Prezzi al " + str(date.today())] = [float(price.replace(' €', '').replace(',', '.')) for price in prices]
        df.to_excel(excel_file, sheet_name=sheet_name)
        adapt_columns(excel_file, sheet_name)

        print("\n\n" + df.to_string())

        x = df.index.values.tolist()
        y = df.values.tolist()

        plt.xticks(range(len(x)), x)
        plt.plot(y)
        plt.ylabel("€")
        plt.grid()

        plt.legend(col, bbox_to_anchor=(0.5, 1.2), loc='upper center', ncol=2)
        plt.tight_layout()

        plt.gcf().autofmt_xdate()
        plt.show()
        plt.draw()


if __name__ == "__main__":
    app = Home()
    app.mainloop()
    """
    get_prices("BDS", "BGY", ["2024-05-15"], '1')
    get_prices("BDS", "MXP", ["2024-05-15"], '1')
    get_prices("BGY", "BDS", ["2024-05-20"], '1')
    get_prices("MXP", "BDS", ["2024-05-20"], '1')
    """