from ..types import Post
from .archive import archiver
from .common import SELENIUM_EXCEPTIONS, click_button
from .config import settings
from selenium.webdriver.common.action_chains import ActionChains

import time

# Used as a threshold to avoid running forever
MAX_POSTS = settings["MAX_POSTS"]

def delete_posts(driver,
                 user_profile_url,
                 year=None):
    """
    Deletes or hides all posts from the wall

    Args:
        driver: seleniumrequests.Chrome Driver instance
        user_profile_url: str
        year: optional int YYYY year
    """

    if year is not None:
        user_profile_url = "{0}/timeline?year={1}".format(user_profile_url, year)

    driver.get(user_profile_url)

    for _ in range(MAX_POSTS):
        post_button_sel = "_4xev"

        post_content_sel = "userContent"
        post_timestamp_sel = "timestampContent"

        button_types = ["FeedDeleteOption", "HIDE_FROM_TIMELINE", "UNTAG"]

        with archiver("wall") as archive_wall_post:
            while True:
                try:
                    timeline_element = driver.find_element_by_class_name(post_button_sel)

                    post_content_element = driver.find_element_by_class_name(post_content_sel)
                    post_content_ts = driver.find_element_by_class_name(post_timestamp_sel)


                    # Archive the post
                    archive_wall_post.archive(
                        Post(
                            content=post_content_element.text,
                            date=post_content_ts.text
                        )
                    )

                    actions = ActionChains(driver)
                    actions.move_to_element(timeline_element).click().perform()

                    menu = driver.find_element_by_css_selector("#globalContainer > div.uiContextualLayerPositioner.uiLayer > div")
                    actions.move_to_element(menu).perform()

                    delete_button = None

                    for button_type in button_types:
                        try:
                            delete_button = menu.find_element_by_xpath("//a[@data-feed-option-name=\"{0}\"]".format(button_type))
                            break
                        except SELENIUM_EXCEPTIONS:
                            continue

                    if not delete_button:
                        print("Could not find anything to delete")
                        break

                    actions.move_to_element(delete_button).click().perform()
                    confirmation_button = driver.find_element_by_class_name("layerConfirm")

                    click_button(driver, confirmation_button)

                except SELENIUM_EXCEPTIONS:
                    continue
                else:
                    break

            # Required to sleep the thread for a bit after using JS to click this button
            time.sleep(5)
            driver.refresh()
