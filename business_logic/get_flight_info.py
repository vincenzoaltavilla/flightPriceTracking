from bs4 import BeautifulSoup
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium import webdriver
from selenium.common.exceptions import TimeoutException, WebDriverException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from webdriver_manager.chrome import ChromeDriverManager
from time import sleep


# From Ryanair URL flight(s), this function returns its(theirs) price(s)
def get_flight_info(url):
    # Software which navigates with Chrome
    chrome_driver = ChromeDriverManager().install()
    op = webdriver.ChromeOptions()
    op.add_experimental_option('excludeSwitches', ['enable-logging'])
    op.add_argument("--silent")
    op.add_argument("--disable-gpu")
    op.add_argument("--log-level=3")
    op.add_argument("--disable-extensions")
    op.add_argument("test-type")
    op.add_argument('headless')

    try:
        # Driver to give orders to Chrome
        driver = webdriver.Chrome(options=op, service=Service(chrome_driver))
        # Open browser at URL
        driver.get(url)
        WebDriverWait(driver, 10).until(ec.presence_of_element_located((By.TAG_NAME, "a")))
        sleep(5)
        # Getting HTML source
        html = driver.page_source

    except TimeoutException:
        print("Timeout.")
    except WebDriverException:
        print("WebDriverError.")
    except Exception as e:
        print("Error:", e)
    else:
        soup = BeautifulSoup(html, 'html.parser')

        if len(soup.find_all('flights-price-simple')):
            times = []
            prices = []

            for flight_price in soup.find_all('flights-price-simple'):
                if 'flight-card-summary__old-value' not in flight_price.parent.get('class', []):
                    prices.append(flight_price.getText(strip=True))
            for flight_time in soup.find_all('span', class_='flight-info__hour'):
                times.append(flight_time.get_text(strip=True))

            info = []

            for i in range(len(prices)):
                info.append({"Departure": times[i * 2], "Arrival": times[i * 2 + 1], "Price": prices[i]})

            return info
        else:
            print('No flights')
            return 0
    finally:
        # Closing browser
        driver.quit()