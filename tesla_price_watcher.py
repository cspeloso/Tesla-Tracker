import re
import requests
import time
import logging
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
import configparser

# Load config ini
config = configparser.ConfigParser()
config.read('config.ini')

LOG_FILE = config['files']['log']
SENT_CARS_FILE = config['files']['sent_cars']
TESLA_MODEL_Y_URL = config['urls']['tesla_model_y']
TESLA_MODEL_3_URL = config['urls']['tesla_model_3']
PUSHOVER_API_URL = config['pushover']['api_url']
PUSHOVER_USER_KEY = config['pushover']['user_key']
PUSHOVER_API_TOKEN = config['pushover']['api_token']
CAR_PRICE_MAX = int(config['settings']['car_price_max'])
DEBUG = config['settings']['debug']


# Logging
logging.basicConfig(filename=LOG_FILE, level=logging.INFO, format='%(asctime)s %(levelname)s:%(message)s')



def logPrint(message):
    """Prints the message if debug mode is enabled."""
    logging.info(message)

    if DEBUG:
        print(message)
    

def send_push_notification(message, car_price, car_selection):
    """Sends a push notification using Pushover."""

    logPrint(f"Sending notification for ${car_price:,.2f} {car_selection}")

    data = {
        "token": PUSHOVER_API_TOKEN,
        "user": PUSHOVER_USER_KEY,
        "message": message
    }
    response = requests.post(PUSHOVER_API_URL, data=data)

    if response.status_code == 200:
        logPrint("Notification sent successfully.")
    else:
        logPrint(f"Failed to send notification. Status code: {response.status_code}")

def car_already_notified(car_link):
    """Checks if a car has already been notified."""
    try:
        with open(SENT_CARS_FILE, 'r') as file:
            sent_cars = file.read().splitlines()
        return car_link in sent_cars
    except FileNotFoundError:
        return False

def mark_car_as_notified(car_link):
    """Marks a car as notified."""
    with open(SENT_CARS_FILE, 'a') as file:
        file.write(car_link + '\n')

def get_car_price(car_section):
    """Gets car price from a car section."""
    car_price_str = car_section.find_element(By.CLASS_NAME, "result-purchase-price").get_attribute("innerHTML")
    return int(car_price_str.replace('$', '').replace(',', ''))

def get_car_link(car_section, specifyModel):
    """Gets the link to the car from a car section."""
    car_data_id = car_section.get_attribute('data-id')
    match = re.match(r"^(.*?)-search-result-container", car_data_id).group(1)
    return f"https://www.tesla.com/m{specifyModel}/order/7SAY{match}?postal=02910&range=200&region=RI&coord=41.7803391,-71.4358733&titleStatus=new&redirect=no#overview"

def get_car_specification(car_section):
    """Gets the car's specification (Standard, LR, Performance)."""
    car_specification_text = car_section.find_element(By.CLASS_NAME, "tds-text_color--10")
    return car_specification_text.get_attribute("innerHTML")

def watch_tesla(TESLA_URL, specifyModel):
    """Main function to watch Tesla car prices."""
    logPrint('Beginning watch_tesla...')

    # Set up Selenium WebDriver
    options = webdriver.ChromeOptions()
    options.add_argument('--no-sandbox')
    options.add_argument('--headless')
    options.add_argument('--ignore-certificate-errors')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument('--disable-extensions')
    options.add_argument('--disable-gpu')
    user_agent = 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.50 Safari/537.36'
    options.add_argument(f'user-agent={user_agent}')
    # options.add_argument('executable_path=/usr/local/bin/chromedriver')

    driver = webdriver.Chrome(executable_path='/usr/local/bin/chromedriver',options=options)
    driver.set_page_load_timeout(90)

    logPrint(f'Loading the Tesla URL: {TESLA_URL}')
    driver.get(TESLA_URL)

    try:

        results_container = WebDriverWait(driver, 100).until(
            EC.presence_of_element_located((By.CLASS_NAME, "results-container"))
        )

        time.sleep(5)

        car_sections = results_container.find_elements(By.CLASS_NAME, "result")

        for car_section in car_sections:

            car_price = get_car_price(car_section)

            if car_price < CAR_PRICE_MAX:

                car_link = get_car_link(car_section, specifyModel)

                if not car_already_notified(car_link):

                    car_specification = get_car_specification(car_section)

                    notification_text = f"SPEC: {car_specification}\n\nPRICE: ${car_price:,.2f}\n\nLINK: {car_link}"

                    send_push_notification(notification_text, car_price, car_specification)

                    mark_car_as_notified(car_link)

    except Exception as e:
        logging.ERROR(f"An error occurred: {e}")
        return False
    finally:
        driver.quit()

    return True

if __name__ == "__main__":

    # Look for model Ys
    run_success = watch_tesla(TESLA_MODEL_Y_URL, 'y')
    if run_success:
        print("Ran successfully for Model Y.")
    else:
        print("Something went wrong.")

    # Look for model 3s
    run_success = watch_tesla(TESLA_MODEL_3_URL, '3')
    if run_success:
        print("Ran successfully for Model 3.")
    else:
        print("Something went wrong.")

