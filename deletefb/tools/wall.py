import time

from selenium.webdriver.chrome.options import Options
from seleniumrequests import Chrome
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import NoSuchElementException, StaleElementReferenceException

MAX_POSTS = 5000
SELENIUM_EXCEPTIONS = (NoSuchElementException, StaleElementReferenceException)

def delete_posts(driver):
    """
    Deletes or hides all posts from the wall
    """
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
