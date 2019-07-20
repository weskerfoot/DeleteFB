from .archive import archiver
from ..types import Conversation
from .common import SELENIUM_EXCEPTIONS, logger
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.action_chains import ActionChains
from pendulum import now

LOG = logger(__name__)

def get_conversations(driver):
    """
    Get a list of conversations
    """

    actions = ActionChains(driver)

    wait = WebDriverWait(driver, 20)

    try:
        wait.until(
            EC.presence_of_element_located((By.XPATH, "//div[@id=\"threadlist_rows\"]"))
        )
    except SELENIUM_EXCEPTIONS:
        LOG.exception("No conversations")
        return

    # This function *cannot* be a generator
    # Otherwise elements will become stale
    conversations = []

    while True:
        for convo in driver.find_elements_by_xpath("//a"):
            url = convo.get_attribute("href")

            timestamp = None

            if url and "messages/read" in url:

                timestamp = convo.find_element_by_xpath("../../..//abbr").text
                conversation_name = convo.find_element_by_xpath("../../../div/div/header/h3").text.strip()

                assert(conversation_name)
                assert(url)

                conversations.append(
                    Conversation(
                        url=url,
                        timestamp=timestamp,
                        name=conversation_name
                    )
                )

        try:
            next_url = (driver.find_element_by_id("see_older_threads").
                        find_element_by_xpath("a").
                        get_attribute("href"))

        except SELENIUM_EXCEPTIONS:
            break
        if not next_url:
            break
        driver.get(next_url)

    return conversations

def delete_conversations(driver, year=None):
    """
    Remove all conversations within a specified range
    """

    driver.get("https://mobile.facebook.com/messages/?pageNum=1&selectable&see_older_newer=1")

    convos = get_conversations(driver)

    for convo in convos:
        # If the year is set and there is a timestamp
        # Then we want to only look at convos from this year

        if year and convo.timestamp:
            if convo.timestamp.year == int(year):
                print(convo)

        # Otherwise we're looking at all convos
        elif not year:
            print(convo)

