from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from .common import SELENIUM_EXCEPTIONS, archiver

def load_likes(driver):
    """
    Loads the page that lists all pages you like
    """
    driver.get("https://www.facebook.com/pages/?category=liked")

    wait = WebDriverWait(driver, 20)

    try:
        wait.until(
            EC.presence_of_element_located((By.XPATH, "//button/div/div[text()='Liked']"))
        )

        wait.until(
            EC.presence_of_element_located((By.XPATH, "//button/div/i[@aria-hidden=\"true\"]"))
        )
    except SELENIUM_EXCEPTIONS:
        return

def unlike_pages(driver):
    """
    Unlike all pages
    """

    like_log, archive_likes = archiver("likes")

    actions = ActionChains(driver)

    load_likes(driver)

    pages_list = driver.find_element_by_css_selector("#all_liked_pages")

    actions.move_to_element(pages_list).perform()

    unlike_buttons = pages_list.find_elements_by_xpath("//button/div/div[text()='Liked']/../..")

    while unlike_buttons:
        for button in unlike_buttons:
            try:
                if "Liked" in button.text:
                    page_name = button.find_element_by_xpath("./../..").text.split("\n")[0]

                    driver.execute_script("arguments[0].click();", button)

                    archive_likes(page_name)

                    print("{0} was unliked".format(page_name))

            except SELENIUM_EXCEPTIONS as e:
                continue

        load_likes(driver)
        try:
            pages_list = driver.find_element_by_css_selector("#all_liked_pages")
            actions.move_to_element(pages_list).perform()
            unlike_buttons = pages_list.find_elements_by_xpath("//button")
            if not unlike_buttons:
                break
        except SELENIUM_EXCEPTIONS:
            break

    # Explicitly close the log file when we're done with it
    like_log.close()
