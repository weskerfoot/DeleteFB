import time

from selenium.webdriver.chrome.options import Options
from seleniumrequests import Chrome
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import NoSuchElementException, StaleElementReferenceException

def login(user_email_address,
          user_password,
          user_profile_url,
          is_headless):
    """
    Attempts to log into Facebook
    Returns a driver object

    user_email_address: str Your Email
    user_password: str Your password
    user_profile_url: str Your profile URL

    """
    # The Chrome driver is required because Gecko was having issues
    chrome_options = Options()
    prefs = {"profile.default_content_setting_values.notifications": 2, 'disk-cache-size': 4096}
    chrome_options.add_experimental_option("prefs", prefs)
    chrome_options.add_argument("start-maximized")

    if is_headless:
        chrome_options.add_argument('--headless')
        chrome_options.add_argument('--disable-gpu')
        chrome_options.add_argument('log-level=2')

    driver = Chrome(options=chrome_options)
    driver.implicitly_wait(10)

    driver.get("https://facebook.com")

    email = "email"
    password = "pass"
    login = "loginbutton"

    emailelement = driver.find_element_by_name(email)
    passwordelement = driver.find_element_by_name(password)

    emailelement.send_keys(user_email_address)
    passwordelement.send_keys(user_password)

    loginelement = driver.find_element_by_id(login)
    loginelement.click()

    if "Two-factor authentication" in driver.page_source:
        # Allow time to enter 2FA code
        print("Pausing to enter 2FA code")
        time.sleep(20)
        print("Continuing execution")
    driver.get(user_profile_url)

    return driver
