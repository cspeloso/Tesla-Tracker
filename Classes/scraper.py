import re
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from notification import send_push_notification
from utils import log_print, car_already_notified, mark_car_as_notified, get_car_price, get_car_link, get_car_specification

def setup_driver(config):
    options = webdriver.ChromeOptions()
    options.add_argument('--no-sandbox')
    options.add_argument('--headless')
    options.add_argument('--disable-gpu')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument('--disable-extensions')
    options.add_argument('--ignore-certificate-errors')
    options.add_argument('--window-size=1920x1080')
    user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.50 Safari/537.36'
    options.add_argument(f'user-agent={user_agent}')
    options.add_argument('--disable-blink-features=AutomationControlled')
    options.add_experimental_option('useAutomationExtension', False)
    options.add_experimental_option('excludeSwitches', ['enable-automation'])

    driver = webdriver.Chrome(executable_path='/usr/local/bin/chromedriver', options=options)
    driver.execute_cdp_cmd('Network.setUserAgentOverride', {"userAgent": user_agent})
    driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
    driver.set_page_load_timeout(90)
    return driver

def watch_tesla(config, specify_model):
    log_print(config, 'Beginning watch_tesla...')
    driver = setup_driver(config)
    tesla_url = config['urls'][f'tesla_model_{specify_model}']

    log_print(config, f'Loading the Tesla URL: {tesla_url}')
    driver.get(tesla_url)
    log_print(config, f'Finished loading Tesla URL.')

    # page_source = driver.page_source
    # log_print(config, page_source)

    try:
        # time.sleep(3)
        log_print(config, f'Scanning webpage...')
        results_container = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, "results-container"))
        )
        log_print(config, f'Finished scanning webpage.')

        # time.sleep(2)
        car_sections = results_container.find_elements(By.CLASS_NAME, "result")

        for car_section in car_sections:
            car_price = get_car_price(car_section)
            if car_price < int(config['settings']['car_price_max']):
                car_link = get_car_link(car_section, specify_model)
                if not car_already_notified(config, car_link):
                    car_specification = get_car_specification(car_section)
                    notification_text = f"SPEC: {car_specification}\n\nPRICE: ${car_price:,.2f}\n\nLINK: {car_link}"
                    send_push_notification(config, notification_text, car_price, car_specification)
                    mark_car_as_notified(config, car_link)

    except Exception as e:
        log_print(config, f"An error occurred: {e}")
        driver.quit()
        return False
    finally:
        driver.quit()

    return True