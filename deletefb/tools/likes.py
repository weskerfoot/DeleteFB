from time import sleep 
from selenium.webdriver.common.action_chains import ActionChains
from .common import SELENIUM_EXCEPTIONS

def unlike_pages(driver,
                 user_profile_url):
    """
    Unlike all pages
    """

    actions = ActionChains(driver)

    driver.get("https://www.facebook.com/pages/?category=liked")

    pages_list = driver.find_element_by_css_selector("#all_liked_pages")

    actions.move_to_element(pages_list)

    unlike_buttons = pages_list.find_elements_by_xpath("//button")

    for button in unlike_buttons:
        print(button)

    sleep(1000)
