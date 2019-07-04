from .archive import archiver
from ..types import Conversation
from .common import SELENIUM_EXCEPTIONS, logger, click_button
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.action_chains import ActionChains

LOG = logger(__name__)

def get_conversation_list(driver):
    """
    Get a list of conversations
    """

    actions = ActionChains(driver)

    convos = driver.find_elements_by_xpath("//ul[@aria-label=\"Conversation list\"]/li")

    for convo in convos:
        actions.move_to_element(convo).perform()
        yield convo.find_element_by_xpath("//a")

def delete_conversations(driver):
    """
    Remove all conversations within a specified range
    """

    driver.get("https://www.facebook.com/messages/t/")

    wait = WebDriverWait(driver, 20)

    for convo_url in get_conversation_list(driver):
        print(convo_url.get_property("data-href"))
