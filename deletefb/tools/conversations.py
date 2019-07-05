from .archive import archiver
from ..types import Conversation
from .common import SELENIUM_EXCEPTIONS, logger, scroll_to
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.action_chains import ActionChains

LOG = logger(__name__)

def get_conversation_list(driver, offset=0):
    """
    Get a list of conversations
    """

    actions = ActionChains(driver)

    convos = driver.find_elements_by_xpath("//ul[@aria-label=\"Conversation list\"]/li/div/a[@role=\"link\"]")

    for convo in convos[offset:]:
        actions.move_to_element(convo).perform()
        yield convo
    actions.move_to_element(current_convo).perform()

def get_all_conversations(driver):
    conversation_urls = set()

    current_convo = None

    while True:
        l = len(conversation_urls)

        for convo in get_conversation_list(driver, offset=l):
            url = convo.get_attribute("data-href")
            conversation_urls.add(url)
            current_convo = convo

        if current_convo:
            scroll_to(driver, current_convo)

        print(l)
        print(len(conversation_urls))
        if len(conversation_urls) == l:
            # no more conversations left
            break

    return list(conversation_urls)


def delete_conversations(driver):
    """
    Remove all conversations within a specified range
    """

    driver.get("https://www.facebook.com/messages/t/")

    wait = WebDriverWait(driver, 20)

    for convo_url in get_all_conversations(driver):
        print(convo_url)
