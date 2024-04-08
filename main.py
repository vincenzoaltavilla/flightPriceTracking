from get_flight_info import *
from datetime import date
import pandas as pd
import os
from openpyxl import load_workbook

airportFrom = "TRN"
airportTo = "BDS"
dateOfFlights = ["2024-05-15", "2024-05-16", "2024-05-17"]
nOfPersons = "1"

col = []
prices = []

for dateOfFlight in dateOfFlights:
    URL = "https://www.ryanair.com/it/it/trip/flights/select?adults=" + nOfPersons + "&teens=0&children=0&infants=0&dateOut=" + dateOfFlight + "&dateIn=&isConnectedFlight=false&discount=0&promoCode=&isReturn=false&originIata=" + airportFrom + "&destinationIata=" + airportTo + "&tpAdults=" + nOfPersons + "&tpTeens=0&tpChildren=0&tpInfants=0&tpStartDate=" + dateOfFlight + "&tpEndDate=&tpDiscount=0&tpPromoCode=&tpOriginIata=" + airportFrom + "&tpDestinationIata=" + airportTo + ""

    info = get_flight_info(URL)
    # print(info)

    if info != 'No flights':
        for flight in info:
            col.append(dateOfFlight+", "+flight['Departure']+"-"+flight['Arrival'])
            prices.append(flight['Price'])


prices_new = [float(price.replace(' €', '').replace(',', '.')) for price in prices]

today = str(date.today())
# today = '2024-03-23'

df = pd.DataFrame(index=["Prezzi al " + today], columns=col)
df.loc["Prezzi al " + today] = prices_new

sheet_name = airportFrom+'-'+airportTo
excel_file = sheet_name + '.xlsx'
df.to_excel(excel_file, sheet_name=sheet_name)

wb = load_workbook(excel_file)
ws = wb[sheet_name]
columns = "ABCDEFG"
for column in columns:
    ws.column_dimensions[column].width = 25
wb.save(excel_file)
wb.close()