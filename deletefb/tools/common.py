import json
import os
from os.path import abspath, relpath, split
import time

from selenium.common.exceptions import (
    NoSuchElementException,
    StaleElementReferenceException,
    TimeoutException
)


SELENIUM_EXCEPTIONS = (
    NoSuchElementException,
    StaleElementReferenceException,
    TimeoutException
)

def try_move(actions, el):
    for _ in range(10):
        try:
            actions.move_to_element(el).perform()
        except StaleElementReferenceException:
            time.sleep(5)
            continue


def archiver(category):
    """
     Log content to file. Call using `archive("some content")`

    Args:
        category: str The category of logs you want to log

    Returns:
        (log_file_handle, archiver)
    """
    log_path = "{0}.log".format(abspath(relpath(split(category)[-1], ".")))

    log_file = open(log_path, mode="ta", buffering=1)

    def log(content, timestamp=False):
        if os.environ.get("DELETEFB_ARCHIVE", "true") == "false":
            return
        structured_content = {
            "category" : category,
            "content" : content,
            "timestamp" : timestamp
        }

        log_file.write("{0}\n".format(json.dumps(structured_content)))

    return (log_file, log)


NO_CHROME_DRIVER = """
You need to install the chromedriver for Selenium\n
Please see this link https://github.com/weskerfoot/DeleteFB#how-to-use-it\n
"""
