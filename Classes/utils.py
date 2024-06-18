import logging
import re
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait

def log_print(config, message):
    logging.info(message)
    if config['settings']['debug']:
        print(message)

def car_already_notified(config, car_link):
    try:
        with open(config['files']['sent_cars'], 'r') as file:
            sent_cars = file.read().splitlines()
        return car_link in sent_cars
    except FileNotFoundError:
        return False

def mark_car_as_notified(config, car_link):
    with open(config['files']['sent_cars'], 'a') as file:
        file.write(car_link + '\n')

def get_car_price(car_section):
    car_price_str = car_section.find_element(By.CLASS_NAME, "result-purchase-price").get_attribute("innerHTML")
    return int(car_price_str.replace('$', '').replace(',', ''))

def get_car_link(car_section, specify_model):
    car_data_id = car_section.get_attribute('data-id')
    match = re.match(r"^(.*?)-search-result-container", car_data_id).group(1)
    return f"https://www.tesla.com/m{specify_model}/order/7SAY{match}?postal=02910&range=200&region=RI&coord=41.7803391,-71.4358733&titleStatus=new&redirect=no#overview"

def get_car_specification(car_section):
    car_specification_text = car_section.find_element(By.CLASS_NAME, "tds-text_color--10")
    return car_specification_text.get_attribute("innerHTML")