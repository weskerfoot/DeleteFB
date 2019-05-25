import time

from selenium.webdriver.chrome.options import Options
from seleniumrequests import Chrome

def login(user_email_address,
          user_password,
          user_profile_url,
          is_headless,
          two_factor_token):
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
    approvals_code = "approvals_code"

    emailelement = driver.find_element_by_name(email)
    passwordelement = driver.find_element_by_name(password)

    emailelement.send_keys(user_email_address)
    passwordelement.send_keys(user_password)

    loginelement = driver.find_element_by_id(login)
    loginelement.click()

    if "two-factor authentication" in driver.page_source.lower():
        if two_factor_token:

            twofactorelement = driver.find_element_by_name(approvals_code)
            twofactorelement.send_keys(two_factor_token)

            # Submits after the code is passed into the form, does not validate 2FA code.
            contelement = driver.find_element_by_id("checkpointSubmitButton")
            contelement.click()

            # Defaults to saving this new browser, this occurs on each new automated login.
            save_browser = driver.find_element_by_id("checkpointSubmitButton")
            save_browser.click()
        else:
            # Allow time to enter 2FA code
            print("Pausing to enter 2FA code")
            time.sleep(20)
            print("Continuing execution")

    driver.get(user_profile_url)
    return driver
