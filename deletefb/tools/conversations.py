from .archive import archiver
from ..types import Conversation, Message
from .common import SELENIUM_EXCEPTIONS, logger, click_button, wait_xpath
from .config import settings
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import Select
from pendulum import now
from json import loads

import lxml.html as lxh

LOG = logger(__name__)

def get_conversations(driver):
    """
    Get a list of conversations
    """

    wait_xpath(driver, "//div[@id=\"threadlist_rows\"]")

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

def parse_conversation(driver):
    """
    Extracts all messages in a conversation
    """

    for msg in lxh.fromstring(driver.page_source).xpath("//div[@class='msg']/div"):
        data_store = loads(msg.get("data-store"))
        msg_text = msg.text_content()

        yield Message(
                name=data_store.get("author"),
                content=msg_text,
                date=data_store.get("timestamp")
              )

def get_images(driver):
    """
    Gets all links to images in a messenger conversation
    Removes duplicates
    """
    for img in set(lxh.fromstring(driver.page_source).xpath("//img")):
        yield img.get("src")

def get_convo(driver, convo):
    """
    Get all of the messages/images for a given conversation
    Returns a list of messages and a list of image links
    """
    driver.get(convo.url)

    wait_xpath(driver, "//*[contains(text(), 'See Older Messages')]")

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

    messages = list(parse_conversation(driver))
    image_links = list(set(get_images(driver)))
    return (messages, image_links)

def delete_conversation(driver, convo):
    """
    Deletes a conversation
    """

    actions = ActionChains(driver)

    menu_select = Select(driver.find_element_by_xpath("//select/option[contains(text(), 'Delete')]/.."))

    for i, option in enumerate(menu_select.options):
        if option.text.strip() == "Delete":
            menu_select.select_by_index(i)
            break

    wait_xpath(driver, "//h2[contains(text(), 'Delete conversation')]")
    delete_button = driver.find_element_by_xpath("//a[contains(text(), 'Delete')][@role='button']")
    actions.move_to_element(delete_button).click().perform()

    return

def extract_convo(driver, convo):
    """
    Extract messages and image links from a conversation
    Return a new Conversation instance
    """
    result = get_convo(driver, convo)

    if not result:
        return None

    messages, image_links = result

    convo.messages = messages
    convo.image_links = image_links

    return convo

def traverse_conversations(driver, year=None):
    """
    Remove all conversations within a specified range
    """

    driver.get("https://mobile.facebook.com/messages/?pageNum=1&selectable&see_older_newer=1")

    convos = get_conversations(driver)

    with archiver("conversations") as archive_convo:
        for convo in convos:
            # If the year is set and there is a date
            # Then we want to only look at convos from this year

            if year and convo.date:
                if convo.date.year == int(year):
                    extract_convo(driver, convo)

                    if settings["ARCHIVE"]:
                        archive_convo.archive(convo)

                    delete_conversation(driver, convo)

            # Otherwise we're looking at all convos
            elif not year:
                extract_convo(driver, convo)

                if settings["ARCHIVE"]:
                    archive_convo.archive(convo)

                delete_conversation(driver, convo)

