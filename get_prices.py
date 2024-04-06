from bs4 import BeautifulSoup
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


# From Ryanair URL flight(s), this function returns its(theirs) price(s)
def get_prices(url):
    # Software which navigates with Chrome
    chrome_driver = ChromeDriverManager().install()
    op = webdriver.ChromeOptions()
    op.add_argument('headless')

    # What we are going to use to give orders to Chrome
    driver = webdriver.Chrome(options=op, service=Service(chrome_driver))

    # Open browser at URL
    driver.get(url)

    element = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, 'flights-price-simple'))
    )

    # Getting HTML source
    html = driver.page_source

    # Closing browser
    driver.quit()

    soup = BeautifulSoup(html, 'html.parser')
    flights = soup.find_all('flights-price-simple')

    prices = []

    if len(flights) == 0:
        return 'No flights'
    else:
        for flight in flights:
            prices.append(flight.getText(strip=True))
        return prices
