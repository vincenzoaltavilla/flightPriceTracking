from get_flight_info import *
from datetime import date
from openpyxl import load_workbook
import pandas as pd
import os
import matplotlib.pyplot as plt

airportFrom = "TRN"
airportTo = "BDS"
dateOfFlights = ["2024-05-15", "2024-05-16", "2024-05-17"]
nOfPersons = "1"

col = []
prices = []

today = str(date.today())
# today = '2024-03-23'

sheet_name = airportFrom+'-'+airportTo
excel_file = sheet_name + '.xlsx'

for dateOfFlight in dateOfFlights:
    print("\n\nAnalizzando voli in data " + dateOfFlight)
    info = get_flight_info("https://www.ryanair.com/it/it/trip/flights/select?adults=" + nOfPersons + "&teens=0&children=0&infants=0&dateOut=" + dateOfFlight + "&dateIn=&isConnectedFlight=false&discount=0&promoCode=&isReturn=false&originIata=" + airportFrom + "&destinationIata=" + airportTo + "&tpAdults=" + nOfPersons + "&tpTeens=0&tpChildren=0&tpInfants=0&tpStartDate=" + dateOfFlight + "&tpEndDate=&tpDiscount=0&tpPromoCode=&tpOriginIata=" + airportFrom + "&tpDestinationIata=" + airportTo + "")

    if info != 'No flights':
        for flight in info:
            col.append(dateOfFlight+", "+flight['Departure']+"-"+flight['Arrival'])
            prices.append(flight['Price'])

if os.path.exists(excel_file):
    df = pd.read_excel(excel_file, sheet_name=sheet_name, index_col=0)
else:
    df = pd.DataFrame(index=["Prezzi al " + today], columns=col)

df.loc["Prezzi al " + today] = [float(price.replace(' €', '').replace(',', '.')) for price in prices]
df.to_excel(excel_file, sheet_name=sheet_name)

wb = load_workbook(excel_file)
ws = wb[sheet_name]
columns = "ABCDEFGHIJKL"
for column in columns:
    ws.column_dimensions[column].width = 25
wb.save(excel_file)
wb.close()

print(df.to_string())

x = df.index.values.tolist()
y = df.values.tolist()
plt.plot(y)
plt.xticks(range(len(x)), x)
plt.legend(col, bbox_to_anchor=(0.5, 1.2), loc='upper center', ncol=2)
plt.tight_layout()
plt.ylabel("€")
plt.grid()
fig = plt.gcf()
plt.show()
plt.draw()
# fig.savefig('grafico.pdf')

input("Press any key to close...")