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


def scrivi_parole_tra_virgolette(file_input, file_output):
    try:
        with open(file_input, 'r', encoding='utf-8') as file:
            # Leggi tutte le righe del file di input
            righe = file.readlines()

        with open(file_output, 'w', encoding='utf-8') as output_file:
            # Scrivi le righe tra virgolette con uno spazio e duepunti dopo la virgoletta di chiusura
            for riga in righe:
                output_file.write(f'"{riga.strip()}": \"\", \n')

        print(f"Righe tra virgolette con spazio e duepunti scritte nel file '{file_output}'.")
    except FileNotFoundError:
        print("Il file non è stato trovato.")
    except Exception as e:
        print("Si è verificato un errore durante la scrittura del file:", e)


if __name__ == "__main__":
    #app = Home()
    #app.mainloop()

    #get_prices("BDS", "TRN", ["2024-05-15"], '1')
    #get_prices("BDS", "MXP", ["2024-05-15"], '1')
    #get_prices("BGY", "BDS", ["2024-05-20"], '1')
    #get_prices("MXP", "BDS", ["2024-05-20"], '1')

    # Esempio di utilizzo
    file_input = "elenco.txt"  # Assicurati che il percorso sia corretto
    file_output = "righe_tra_virgolette.txt"  # Specifica il nome del file di output
    scrivi_parole_tra_virgolette(file_input, file_output)