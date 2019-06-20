from .archive import archiver
from ..types import Page
from .common import SELENIUM_EXCEPTIONS, logger, click_button
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

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

def get_page_links(driver):
    """
    Gets all of the links to the pages you like

    Args:
        driver: seleniumrequests.Chrome Driver instance
    Returns:
        List of URLs to pages
    """
    pages = driver.find_elements_by_xpath("//li//div/div/a[contains(@class, 'lfloat')]")

    return [page.get_attribute("href").replace("www", "mobile") for page in pages]

def unlike_page(driver, url, archive=None):
    """
    Unlikes a page given the URL to it
    Args:
        driver: seleniumrequests.Chrome Driver instance
        url: url string pointing to a page
        archive: archiver instance

    Returns:
        None

    """

    driver.get(url)

    print("Unliking {0}".format(url))

    wait = WebDriverWait(driver, 20)

    try:
        wait.until(
            EC.presence_of_element_located((By.XPATH, "//*[text()='Liked']"))
        )
    except SELENIUM_EXCEPTIONS:
        # Something went wrong with this page, so skip it
        return

    button = driver.find_element_by_xpath("//*[text()='Liked']")

    # Click the "Liked" button to open up "Unlike"
    click_button(driver, button)

    wait.until(
        EC.presence_of_element_located((By.XPATH, "//*[text()='Unlike']"))
    )

    # There should be an "Unlike" button now, click it
    unlike_button = driver.find_element_by_xpath("//*[text()='Unlike']/..")

    click_button(driver, unlike_button)

    if archive:
        archive(Page(name=url))

def unlike_pages(driver, profile_url):
    """
    Unlike all pages

    Args:
        driver: seleniumrequests.Chrome Driver instance

    Returns:
        None
    """

    with archiver("likes") as archive_likes:
        load_likes(driver, profile_url)

        urls = get_page_links(driver)

        while urls:
            for url in urls:
                unlike_page(driver, url, archive=archive_likes.archive)
            try:
                load_likes(driver, profile_url)
                urls = get_page_links(driver)
            except SELENIUM_EXCEPTIONS:
                # We're done
                break
