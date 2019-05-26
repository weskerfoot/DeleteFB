from time import sleep 
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from .common import SELENIUM_EXCEPTIONS, archiver

def unlike_pages(driver,
                 user_profile_url):
    """
    Unlike all pages
    """

    like_log, archive_likes = archiver("likes")

    actions = ActionChains(driver)

    driver.get("https://www.facebook.com/pages/?category=liked")

    wait = WebDriverWait(driver, 20)

    wait.until(
        EC.presence_of_element_located((By.XPATH, "//div[text()='Liked']"))
    )

    sleep(10)

    pages_list = driver.find_element_by_css_selector("#all_liked_pages")
    actions.move_to_element(pages_list).perform()
    unlike_buttons = pages_list.find_elements_by_xpath("//button")

    for button in unlike_buttons:
        try:
            actions.move_to_element(button).perform()
            page_name = button.find_element_by_xpath("./../..").text.split("\n")[0]
            archive_likes(page_name)

        except SELENIUM_EXCEPTIONS as e:
            print(e)
            continue
        print(button)

    # Explicitly close the log file when we're done with it
    like_log.close()
