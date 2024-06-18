import requests
from utils import log_print

def send_push_notification(config, message, car_price, car_selection):
    log_print(config, f"Sending notification for ${car_price:,.2f} {car_selection}")

    data = {
        "token": config['pushover']['api_token'],
        "user": config['pushover']['user_key'],
        "message": message
    }
    response = requests.post(config['pushover']['api_url'], data=data)

    if response.status_code == 200:
        log_print(config, "Notification sent successfully.")
    else:
        log_print(config, f"Failed to send notification. Status code: {response.status_code}")