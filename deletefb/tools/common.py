from os.path import isfile
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import (
    NoSuchElementException,
    StaleElementReferenceException,
    TimeoutException,
    JavascriptException
)

import json
import logging
import logging.config
import os
import pendulum

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


def wait_xpath(driver, expr):
    """
    Takes an XPath expression, and waits at most 20 seconds until it exists
    """
    wait = WebDriverWait(driver, 20)
    try:
        wait.until(EC.presence_of_element_located((By.XPATH, expr)))
    except SELENIUM_EXCEPTIONS:
        return

NO_CHROME_DRIVER = """
You need to install the chromedriver for Selenium\n
Please see this link https://github.com/weskerfoot/DeleteFB#how-to-use-it\n
"""
