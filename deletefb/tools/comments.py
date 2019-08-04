from .archive import archiver
from ..types import Comment
from .common import SELENIUM_EXCEPTIONS, logger, click_button
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

LOG = logger(__name__)

def delete_comments(driver, profile_url):
    """
    Remove all comments on posts
    """

    driver.get("{0}/allactivity?privacy_source=activity_log&category_key=commentscluster".format(profile_url))

    wait = WebDriverWait(driver, 20)
