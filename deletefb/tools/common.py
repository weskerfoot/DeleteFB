from selenium.common.exceptions import (NoSuchElementException,
                                        StaleElementReferenceException,
                                        TimeoutException)
from time import sleep
from json import dumps
from os.path import abspath, relpath, split

SELENIUM_EXCEPTIONS = (NoSuchElementException,
                       StaleElementReferenceException,
                       TimeoutException)

def try_move(actions, el):
    for _ in range(10):
        try:
            actions.move_to_element(el).perform()
        except StaleElementReferenceException:
            sleep(5)
            continue


def archiver(category):
    """
    category: the category of logs you want to log
    return values: (log_file_handle, archiver)

    call archiver like archive("some content")
    """
    log_path = "{0}.log".format(abspath(relpath(split(category)[-1], ".")))

    log_file = open(log_path, mode="wt", buffering=1)

    def log(content, timestamp=False):
        structured_content = {
                               "category" : category,
                               "content" : content,
                               "timestamp" : timestamp
                              }

        log_file.write("{0}\n".format(dumps(structured_content)))

    return (log_file, log)


no_chrome_driver = """
You need to install the chromedriver for Selenium\n
Please see this link https://github.com/weskerfoot/DeleteFB#how-to-use-it\n
"""
