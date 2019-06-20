from os.path import isfile
from selenium.common.exceptions import (
    NoSuchElementException,
    StaleElementReferenceException,
    TimeoutException
)

import json
import logging
import logging.config
import os

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
