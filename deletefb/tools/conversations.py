from .archive import archiver
from ..types import Conversation
from .common import SELENIUM_EXCEPTIONS, logger, click_button
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

LOG = logger(__name__)

def delete_conversations(driver):
    """
    Remove all conversations within a specified range
    """

    driver.get("https://www.facebook.com/messages/t/")
