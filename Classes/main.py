from config import load_config
from logger import setup_logging
from scraper import watch_tesla

def main():
    config = load_config('config.ini')
    setup_logging(config['files']['log'], config['settings']['debug'])

    run_success = watch_tesla(config, 'y')
    if run_success:
        print("Ran successfully for Model Y.\n\n")
    else:
        print("Something went wrong.\n\n")

    run_success = watch_tesla(config, '3')
    if run_success:
        print("Ran successfully for Model 3.\n\n")
    else:
        print("Something went wrong.\n\n")

if __name__ == "__main__":
    main()