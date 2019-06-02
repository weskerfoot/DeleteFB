from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from .common import SELENIUM_EXCEPTIONS, archiver, logger, click_button

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

    wait = WebDriverWait(driver, 30)

    try:
        wait.until(
            EC.presence_of_element_located((By.CSS_SELECTOR, ".PageLikeButton"))
        )
    except SELENIUM_EXCEPTIONS:
        LOG.exception("Traceback of load_likes")
        return


def get_page_links(driver):
    """
    Gets all of the links to the pages you like

    Args:
        driver: seleniumrequests.Chrome Driver instance
    Returns:
        List of URLs to pages
    """
    pages = driver.find_elements_by_xpath("//li//div/div/a[contains(@class, 'lfloat')]")

    actions = ActionChains(driver)

    return [page.get_attribute("href").replace("www", "mobile") for page in pages]


def unlike_page(driver, url):
    """
    Unlikes a page given the URL to it
    Args:
        driver: seleniumrequests.Chrome Driver instance
        url: url string pointing to a page

    Returns:
        None

    """
    driver.get(url)
    wait = WebDriverWait(driver, 30)

    actions = ActionChains(driver)

    wait.until(
        EC.presence_of_element_located((By.XPATH, "//*[text()='Liked']"))
    )

    button = driver.find_element_by_xpath("//*[text()='Liked']")

    # Click the "Liked" button to open up "Unlike"
    click_button(driver, button)

    wait.until(
        EC.presence_of_element_located((By.XPATH, "//a/span[text()='Unlike']"))
    )

    # There should be an "Unlike" button now, click it
    unlike_button = driver.find_element_by_xpath("//a/span[text()='Unlike']/..")

    click_button(driver, unlike_button)


def unlike_pages(driver, profile_url):
    """
    Unlike all pages

    Args:
        driver: seleniumrequests.Chrome Driver instance

    Returns:
        None
    """

    like_log, archive_likes = archiver("likes")

    load_likes(driver, profile_url)

    urls = get_page_links(driver)

    while urls:
        for url in urls:
            unlike_page(driver, url)
        load_likes(driver, profile_url)
        try:
            urls = get_page_links(driver)
        except SELENIUM_EXCEPTIONS:
            # We're done
            break

    # Explicitly close the log file when we're done with it
    like_log.close()
