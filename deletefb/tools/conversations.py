from .archive import archiver
from ..types import Conversation, Message
from .common import SELENIUM_EXCEPTIONS, logger, click_button
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.action_chains import ActionChains
from pendulum import now
from json import loads

import lxml.html as lxh

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

            date = None

            if url and "messages/read" in url:

                date = convo.find_element_by_xpath("../../..//abbr").text
                conversation_name = convo.find_element_by_xpath("../../../div/div/header/h3").text.strip()

                assert(conversation_name)
                assert(url)

                conversations.append(
                    Conversation(
                        url=url,
                        date=date,
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

def get_convo_images(driver):
    """
    Gets all links to images in a messenger conversation
    Removes duplicates
    """
    for img in set(lxh.fromstring(driver.page_source).xpath("//img")):
        yield img.get("src")

def get_convo_messages(driver):
    """
    Gets all messages in a conversation
    """

    for msg in lxh.fromstring(driver.page_source).xpath("//div[@class='msg']/div"):
        data_store = loads(msg.get("data-store"))
        msg_text = msg.text_content()

        yield Message(
                name=data_store.get("author"),
                content=msg_text,
                date=data_store.get("timestamp")
              )

def archive_conversation(driver, convo):
    print(convo)
    driver.get(convo.url)

    wait = WebDriverWait(driver, 20)
    try:
        wait.until(
                EC.presence_of_element_located((By.XPATH, "//*[contains(text(), 'See Older Messages')]"))
                )
    except SELENIUM_EXCEPTIONS:
        LOG.exception("Could not load more messages")
        return

    # Expand conversation until we've reached the beginning
    while True:
        try:
            see_older = driver.find_element_by_xpath("//*[contains(text(), 'See Older Messages')]")
        except SELENIUM_EXCEPTIONS:
            break

        if not see_older:
            break

        try:
            click_button(driver, see_older)
        except SELENIUM_EXCEPTIONS:
            continue

    #for img in get_convo_images(driver):
        #print(img)

    convo.messages = list(get_convo_messages(driver))

def delete_conversations(driver, year=None):
    """
    Remove all conversations within a specified range
    """

    driver.get("https://mobile.facebook.com/messages/?pageNum=1&selectable&see_older_newer=1")

    convos = get_conversations(driver)

    for convo in convos:
        # If the year is set and there is a date
        # Then we want to only look at convos from this year

        if year and convo.date:
            if convo.date.year == int(year):
                archive_conversation(driver, convo)
                print(convo.messages)

        # Otherwise we're looking at all convos
        elif not year:
            archive_conversation(driver, convo)
