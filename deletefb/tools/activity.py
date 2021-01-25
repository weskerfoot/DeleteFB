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

    print("Loaded")

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

    if year is None:
        print("Deleting all years")
        years = [elem.text.strip() for elem in get_timeslices(driver)]
    else:
        years = [elem.text.strip() for elem in get_timeslices(driver) if year in elem.text.strip()]

    actions = ActionChains(driver)

    print(years)

    for year in years:
        year_elems = [y for y in get_timeslices(driver) if y.text.strip() == year]

        if not year_elems:
            raise ValueError("Non-existent year") # FIXME use a better exception

        year_elem = year_elems[0]

        # Need to figure out how to ignore the ones with nothing in them
        print(f"Deleting activity from {year_elem.text}")

        actions.move_to_element(year_elem)
        year_elem.click()

        get_load_more(driver)

        time.sleep(10)

        driver.refresh()


    #with archiver("activity") as archive_wall_post:
