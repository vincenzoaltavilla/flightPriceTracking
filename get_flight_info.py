from bs4 import BeautifulSoup
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium import webdriver
from time import sleep


# From Ryanair URL flight(s), this function returns its(theirs) price(s)
def get_flight_info(url):
    # Software which navigates with Chrome
    chrome_driver = ChromeDriverManager().install()
    op = webdriver.ChromeOptions()
    op.add_argument('headless')

    # What we are going to use to give orders to Chrome
    driver = webdriver.Chrome(options=op, service=Service(chrome_driver))

    # Open browser at URL
    driver.get(url)
    sleep(5)

    # Getting HTML source
    html = driver.page_source

    # Closing browser
    driver.quit()

    soup = BeautifulSoup(html, 'html.parser')

    flights_prices = soup.find_all('flights-price-simple')
    flights_times = soup.find_all('span', class_='flight-info__hour')
    times = []
    prices = []

    if len(flights_prices) == 0:
        return 'No flights'
    else:
        for flight_price in flights_prices:
            prices.append(flight_price.getText(strip=True))
        for flight_time in flights_times:
            times.append(flight_time.get_text(strip=True))

        info = []

        for i in range(len(prices)):
            flight_info = {"Departure": times[i*2], "Arrival": times[i*2 + 1], "Price": prices[i]}
            info.append(flight_info)

        return info