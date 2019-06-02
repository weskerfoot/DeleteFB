from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from time import sleep

from .common import SELENIUM_EXCEPTIONS, archiver, logger

LOG = logger(__name__)


def load_likes(driver, profile_url):
    """
    Loads the page that lists all pages you like

    Args:
        driver: seleniumrequests.Chrome Driver instance

    Returns:
        None
    """

    driver.get("{0}/likes_all".format(profile_url))

    wait = WebDriverWait(driver, 20)

    try:
        wait.until(
            EC.presence_of_element_located((By.CSS_SELECTOR, ".PageLikeButton"))
        )
    except SELENIUM_EXCEPTIONS:
        LOG.exception("Traceback of load_likes")
        return

def unlike_pages(driver, profile_url):
    """
    Unlike all pages

    Args:
        driver: seleniumrequests.Chrome Driver instance

    Returns:
        None
    """

    like_log, archive_likes = archiver("likes")

    wait = WebDriverWait(driver, 20)
    actions = ActionChains(driver)

    load_likes(driver, profile_url)

    pages = driver.find_elements_by_xpath("//li//div/div/a[contains(@class, 'lfloat')]")

    actions = ActionChains(driver)

    page_urls = [page.get_attribute("href").replace("www", "mobile") for page in pages]

    for url in page_urls:
        driver.get(url)


    # Explicitly close the log file when we're done with it
    like_log.close()
