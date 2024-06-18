try:
    from selenium import webdriver
    from selenium.common.exceptions import WebDriverException

    print("Selenium is installed correctly.")
except ImportError:
    print("Selenium is not installed. Please install it using 'pip install selenium'.")
    exit(1)

def test_chrome_driver():
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')  # Run in headless mode (no GUI)
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')

    try:
        # Update the path to the ChromeDriver if necessary
        driver = webdriver.Chrome(executable_path='/usr/local/bin/chromedriver', options=options)
        driver.get("http://www.google.com")
        
        if "Google" in driver.title:
            print("ChromeDriver is installed and working correctly.")
        else:
            print("ChromeDriver is installed, but there was an issue with loading the page.")

        driver.quit()
    except WebDriverException as e:
        print(f"An error occurred with ChromeDriver: {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

if __name__ == "__main__":
    test_chrome_driver()