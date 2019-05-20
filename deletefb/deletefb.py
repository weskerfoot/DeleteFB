#! /usr/bin/env python

from seleniumrequests import Chrome
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

import time
import argparse

def run_delete():
    parser = argparse.ArgumentParser()
    parser.add_argument("-E",
                        "--email",
                        default=None,
                        help="Your email address associated with the account")

    parser.add_argument("-P",
                        "--password",
                        default=None,
                        help="Your Facebook password")

    parser.add_argument("-U",
                        "--profile-url",
                        default=None,
                        help="""
                        The link to your Facebook profile, e.g. https://www.facebook.com/your.name
                        """)

    args = parser.parse_args()

    delete_posts(user_email_address=args.email,
                 user_password=args.password,
                 user_profile_url=args.profile_url)

def delete_posts(user_email_address=None,
                 user_password=None,
                 user_profile_url=None):
    """
    user_email_address: Your Email
    user_password: Your password
    user_profile_url: Your profile URL
    """

    assert all((user_email_address,
                user_password,
                user_profile_url)), "Insufficient arguments provided"

    chrome_options = Options()
    prefs = {"profile.default_content_setting_values.notifications" : 2}
    chrome_options.add_experimental_option("prefs", prefs)

    chrome_options.add_argument("start-maximized")

    driver = Chrome(chrome_options=chrome_options)

    driver.get("https://facebook.com")

    email = "email"
    password = "pass"
    login="loginbutton"

    emailelement = driver.find_element_by_name(email)

    passwordelement = driver.find_element_by_name(password)

    emailelement.send_keys(user_email_address)

    passwordelement.send_keys(user_password)

    loginelement = driver.find_element_by_id(login)

    loginelement.click()
    time.sleep(3)

    driver.get(user_profile_url)
    time.sleep(3)

    for _ in range(5100):
        post_button_sel = "_4xev"
        timeline_element = driver.find_element_by_class_name(post_button_sel)
        actions = ActionChains(driver)
        actions.move_to_element(timeline_element).click().perform()

        menu_selector = "#globalContainer > div.uiContextualLayerPositioner.uiLayer > div"

        #time.sleep(3)

        menu = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, menu_selector)))

        actions.move_to_element(menu).perform()

        try:
            delete_button = menu.find_element_by_xpath("//a[@data-feed-option-name=\"FeedDeleteOption\"]")
        except:
            delete_button = menu.find_element_by_xpath("//a[@data-feed-option-name=\"HIDE_FROM_TIMELINE\"]")

        actions.move_to_element(delete_button).click().perform()

        time.sleep(4)

        confirmation_button = driver.find_element_by_class_name("layerConfirm")
        driver.execute_script("arguments[0].click();", confirmation_button)
        time.sleep(3)
        driver.refresh()
