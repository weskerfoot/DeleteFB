import json
import logging
import logging.config
import os
import time

from .config import settings

from os.path import abspath, relpath, split, isfile
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

def click_button(driver, el):
    """
    Click a button using Javascript
    Args:
        driver: seleniumrequests.Chrome Driver instance
    Returns:
        None
    """
    driver.execute_script("arguments[0].click();", el)

def logger(name):
    """
    Args:
        name (str): Logger name

    Returns:
        logging.Logger
    """
    config_path = "deletefb/logging_conf.json"
    if not isfile(config_path):  # called from file (deletefb.py)
        os.chdir("..")
    with open(config_path, "r", encoding="utf-8") as config_file:
        config = json.load(config_file)
        logging.config.dictConfig(config["logging"])
    return logging.getLogger(name)

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
        if not settings["ARCHIVE"]:
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
