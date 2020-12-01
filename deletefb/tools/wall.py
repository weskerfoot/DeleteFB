from ..types import Post
from .archive import archiver
from .common import SELENIUM_EXCEPTIONS, click_button, wait_xpath, force_mobile
from .config import settings
from selenium.webdriver.common.action_chains import ActionChains

import time

# Used as a threshold to avoid running forever
MAX_POSTS = settings["MAX_POSTS"]

def delete_posts(driver,
                 user_profile_url):
    """
    Deletes or hides all posts from the wall

    Args:
        driver: seleniumrequests.Chrome Driver instance
        user_profile_url: str
        year: optional int YYYY year
    """

    user_profile_url = force_mobile(user_profile_url)

    driver.get(user_profile_url)

    finished = False

    with archiver("wall") as archive_wall_post:
        for _ in range(MAX_POSTS):
            if finished:
                break
            post_button_sel = "_4s19"

            post_content_sel = "userContent"
            post_timestamp_sel = "timestampContent"

            confirmation_button_exp = "//div[contains(@data-sigil, 'undo-content')]//*/a[contains(@href, 'direct_action_execute')]"

            # Cannot return a text node, so it returns the parent.
            # Tries to be pretty resilient against DOM re-organizations
            timestamp_exp = "//article//*/header//*/div/a[contains(@href, 'story_fbid')]//text()/.."

            button_types = ["Delete post", "Remove tag", "Hide from timeline", "Hide from profile"]

            while True:
                try:
                    try:
                        timeline_element = driver.find_element_by_xpath("//div[@data-sigil='story-popup-causal-init']/a")
                    except SELENIUM_EXCEPTIONS:
                        print("Could not find any posts")
                        finished = True
                        break

                    post_content_element = driver.find_element_by_xpath("//article/div[@class='story_body_container']/div")
                    post_content_ts = driver.find_element_by_xpath(timestamp_exp)

                    if not (post_content_element or post_content_ts):
                        break

                    # Archive the post
                    archive_wall_post.archive(
                        Post(
                            content=post_content_element.text,
                            date=post_content_ts.text
                        )
                    )

                    actions = ActionChains(driver)
                    actions.move_to_element(timeline_element).click().perform()

                    # Wait until the buttons show up
                    wait_xpath(driver, "//*[contains(@data-sigil, 'removeStoryButton')]")

                    delete_button = None

                    # Search for visible buttons in priority order
                    # Delete -> Untag -> Hide
                    for button_type in button_types:
                        try:
                            delete_button = driver.find_element_by_xpath("//*[text()='{0}']".format(button_type))
                            if not delete_button.is_displayed():
                                continue
                            break
                        except SELENIUM_EXCEPTIONS as e:
                            print(e)
                            continue

                    if not delete_button:
                        print("Could not find anything to delete")
                        break

                    click_button(driver, delete_button)
                    wait_xpath(driver, confirmation_button_exp)
                    confirmation_button = driver.find_element_by_xpath(confirmation_button_exp)

                    print(confirmation_button)
                    click_button(driver, confirmation_button)

                except SELENIUM_EXCEPTIONS as e:
                    print(e)
                    continue
                else:
                    break

            # Required to sleep the thread for a bit after using JS to click this button
            time.sleep(5)
            driver.refresh()
