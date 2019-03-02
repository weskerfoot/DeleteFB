#! /usr/bin/env python

from seleniumrequests import Chrome
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.chrome.options import Options
import time

EMAIL_ADDRESS = "Your Email Here"
PASSWORD = "Your Password Here"

PROFILE_URL = "https://www.facebook.com/your.name"

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

emailelement.send_keys(EMAIL_ADDRESS)

passwordelement.send_keys(PASSWORD)

loginelement = driver.find_element_by_id(login)

loginelement.click()
time.sleep(3)

driver.get(PROFILE_URL)
time.sleep(3)

for _ in range(5100):
    post_button_sel = "_4xev"
    timeline_element = driver.find_element_by_class_name(post_button_sel)
    actions = ActionChains(driver)
    actions.move_to_element(timeline_element).click().perform()
    time.sleep(5)

    menu = driver.find_element_by_css_selector("#globalContainer > div.uiContextualLayerPositioner.uiLayer > div")
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
