from os.path import isfile
from selenium.common.exceptions import (
    NoSuchElementException,
    StaleElementReferenceException,
    TimeoutException,
    JavascriptException
)
from arrow.parser import ParserError

import json
import logging
import logging.config
import os
import arrow

SELENIUM_EXCEPTIONS = (
    NoSuchElementException,
    StaleElementReferenceException,
    TimeoutException
)

def click_button(driver, el):
    """
    Click a button using Javascript
    """
    driver.execute_script("arguments[0].click();", el)

def scroll_to(driver, el):
    """
    Scroll an element into view, using JS
    """
    try:
        driver.execute_script("arguments[0].scrollIntoView();", el)
    except SELENIUM_EXCEPTIONS:
        return

def parse_ts(text):
    return arrow.get(text, "DD/M/YYYY")

def logger(name):
    """
    Args:
        name (str): Logger name

    Returns:
        logging.Logger
    """

    # Make sure the path always points to the correct directory
    config_path = os.path.dirname(os.path.realpath(__file__)) + "/../logging_conf.json"

    if not isfile(config_path):  # called from file (deletefb.py)
        os.chdir("..")
    with open(config_path, "r", encoding="utf-8") as config_file:
        config = json.load(config_file)
        logging.config.dictConfig(config["logging"])
    return logging.getLogger(name)

NO_CHROME_DRIVER = """
You need to install the chromedriver for Selenium\n
Please see this link https://github.com/weskerfoot/DeleteFB#how-to-use-it\n
"""
