from .common import NO_CHROME_DRIVER
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.chrome.options import Options
from seleniumrequests import Chrome

import sys
import time

def login(user_email_address,
          user_password,
          is_headless,
          two_factor_token):
    """
    Attempts to log into Facebook
    Returns a driver object

    Args:
        user_email_address: str Your email
        user_password: str Your password
        user_profile_url: str Your profile URL

    Returns:
        seleniumrequests.Chrome instance

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

    try:
        driver = Chrome(options=chrome_options)
    except Exception as e:
        # The user does not have chromedriver installed
        # Tell them to install it
        sys.stderr.write(str(e))
        sys.stderr.write(NO_CHROME_DRIVER)
        sys.exit(1)

    driver.implicitly_wait(10)

    driver.get("https://www.facebook.com/login/device-based/regular/login/?login_attempt=1&lwv=110")

    email = "email"
    password = "pass"
    login_button = "loginbutton"
    approvals_code = "approvals_code"

    emailelement = driver.find_element_by_name(email)
    passwordelement = driver.find_element_by_name(password)

    emailelement.send_keys(user_email_address)
    passwordelement.send_keys(user_password)

    loginelement = driver.find_element_by_id(login_button)
    loginelement.click()

    # Defaults to no 2fa
    has_2fa = False

    try:
        # If this element exists, we've reached a 2FA page
        driver.find_element_by_xpath("//form[@class=\"checkpoint\"]")
        driver.find_element_by_xpath("//input[@name=\"approvals_code\"]")
        has_2fa = True
    except NoSuchElementException:
        has_2fa = "two-factor authentication" in driver.page_source.lower() or has_2fa

    if has_2fa:
        print("""
            Two-Factor Auth is enabled.
            Please file an issue at https://github.com/weskerfoot/DeleteFB/issues if you run into any problems
        """)

    if two_factor_token and has_2fa:
        twofactorelement = driver.find_element_by_name(approvals_code)
        twofactorelement.send_keys(two_factor_token)

        # Submits after the code is passed into the form, does not validate 2FA code.
        contelement = driver.find_element_by_id("checkpointSubmitButton")
        contelement.click()

        # Defaults to saving this new browser, this occurs on each new automated login.
        save_browser = driver.find_element_by_id("checkpointSubmitButton")
        save_browser.click()
    elif has_2fa:
        # Allow time to enter 2FA code
        print("Pausing to enter 2FA code")
        time.sleep(35)
        print("Continuing execution")
    else:
        pass

    # block until we have reached the main page
    # print a message warning the user
    while driver.current_url != "https://www.facebook.com/":
        print("Execution blocked: Please navigate to https://www.facebook.com to continue")
        time.sleep(5)

    return driver
