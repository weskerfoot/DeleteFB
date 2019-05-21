#! /usr/bin/env python

import argparse
import time

from seleniumrequests import Chrome
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import NoSuchElementException, StaleElementReferenceException

MAX_POSTS = 5000
SELENIUM_EXCEPTIONS = (NoSuchElementException, StaleElementReferenceException)

def run_delete():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-E",
        "--email",
        required=True,
        dest="email",
        type=str,
        help="Your email address associated with the account"
    )

    parser.add_argument(
        "-P",
        "--password",
        required=True,
        dest="password",
        type=str,
        help="Your Facebook password"
    )

    parser.add_argument(
        "-U",
        "--profile-url",
        required=True,
        dest="profile_url",
        type=str,
        help="The link to your Facebook profile, e.g. https://www.facebook.com/your.name"
    )

    parser.add_argument(
        "-H",
        "--headless",
        action="store_true",
        dest="is_headless",
        default=False,
        help="Run browser in headless mode (no gui)"
    )

    args = parser.parse_args()

    delete_posts(
        user_email_address=args.email,
        user_password=args.password,
        user_profile_url=args.profile_url,
        is_headless=args.is_headless
    )

def delete_posts(user_email_address,
                 user_password,
                 user_profile_url,
                 is_headless):
    """
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

    for _ in range(MAX_POSTS):
        post_button_sel = "_4xev"

        while True:
            try:
                timeline_element = driver.find_element_by_class_name(post_button_sel)
                actions = ActionChains(driver)
                actions.move_to_element(timeline_element).click().perform()

                menu = driver.find_element_by_css_selector("#globalContainer > div.uiContextualLayerPositioner.uiLayer > div")
                actions.move_to_element(menu).perform()

                try:
                    delete_button = menu.find_element_by_xpath("//a[@data-feed-option-name=\"FeedDeleteOption\"]")
                except SELENIUM_EXCEPTIONS:
                    delete_button = menu.find_element_by_xpath("//a[@data-feed-option-name=\"HIDE_FROM_TIMELINE\"]")

                actions.move_to_element(delete_button).click().perform()
                confirmation_button = driver.find_element_by_class_name("layerConfirm")

                # Facebook would not let me get focus on this button without some custom JS
                driver.execute_script("arguments[0].click();", confirmation_button)
            except SELENIUM_EXCEPTIONS:
                continue
            else:
                break

        # Required to sleep the thread for a bit after using JS to click this button
        time.sleep(5)
        driver.refresh()


if __name__ == "__main__":
    run_delete()
