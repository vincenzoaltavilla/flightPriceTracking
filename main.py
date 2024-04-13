from get_flight_info import *
from format import *
from datetime import date
import pandas as pd
import os
import matplotlib.pyplot as plt
import matplotlib.backends.backend_pdf
import keyboard


def main():
    airportFrom = "TRN"
    airportTo = "BDS"
    dateOfFlights = ["2024-05-15", "2024-05-16", "2024-05-17"]
    nOfPersons = '1'

    sheet_name = airportFrom + '-' + airportTo
    excel_file = sheet_name + "-" + ",".join(dateOfFlights) + ".xlsx"

    col, prices = [], []

    for dateOfFlight in dateOfFlights:
        print("\n\nAnalizzando voli in data " + dateOfFlight)
        URL = f"https://www.ryanair.com/it/it/trip/flights/select?adults={nOfPersons}&teens=0&children=0&infants=0&dateOut={dateOfFlight}&dateIn=&isConnectedFlight=false&discount=0&promoCode=&isReturn=false&originIata={airportFrom}&destinationIata={airportTo}&tpAdults={nOfPersons}&tpTeens=0&tpChildren=0&tpInfants=0&tpStartDate={dateOfFlight}&tpEndDate=&tpDiscount=0&tpPromoCode=&tpOriginIata={airportFrom}&tpDestinationIata={airportTo}"
        # print(URL)

        info = get_flight_info(URL)

        if info:
            for flight in info:
                col.append(dateOfFlight + ", " + flight['Departure'] + "-" + flight['Arrival'])
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

        print("\n\n"+ df.to_string())

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

        print("\n\n\nPress any key to close...")
        keyboard.read_key()

if __name__ == "__main__":
    main()