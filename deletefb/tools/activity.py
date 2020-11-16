from ..types import Post
from .archive import archiver
from .common import SELENIUM_EXCEPTIONS, click_button, wait_xpath, force_mobile
from .config import settings
from selenium.webdriver.common.action_chains import ActionChains
from calendar import month_name

months = [m for m in month_name if m]

import time

# Used as a threshold to avoid running forever
MAX_POSTS = settings["MAX_POSTS"]

def get_load_more(driver):
    """
    Click the "Load more from X" button repeatedly
    """

    button_expr = f"//div[contains(text(), 'Load more from')]"

    print("Trying to load more")

    while True:
        try:
            wait_xpath(driver, button_expr)
            driver.find_element_by_xpath(button_expr).click()
        except SELENIUM_EXCEPTIONS:
            break

def get_timeslices(driver):
    """
    Get a list of the time slices Facebook is going to let us click.
    """

    slice_expr = "//header"

    wait_xpath(driver, slice_expr)
    for ts in driver.find_elements_by_xpath(slice_expr):
        if any(w in months for w in ts.text.strip().split()):
            yield ts
        try:
            int(ts.text.strip())
            if len(ts.text.strip()) == 4: # it's a year
                yield ts
        except ValueError:
            continue

def delete_activity(driver,
                    year=None):
    """
    Deletes or hides all activity related to posts.

    Args:
        driver: seleniumrequests.Chrome Driver instance
        year: optional int YYYY year
    """

    driver.get("https://m.facebook.com/allactivity/?category_key=statuscluster")

    #print(get_load_more(driver))

    actions = ActionChains(driver)

    for ts in get_timeslices(driver):
        # Need to figure out how to ignore the ones with nothing in them
        print(ts.text)
        actions.move_to_element(ts)
        get_load_more(driver)

    time.sleep(1000)

    #with archiver("activity") as archive_wall_post:
