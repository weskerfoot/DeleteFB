import re
import zipfile
import os, sys, stat, platform
from urllib.request import urlretrieve

from clint.textui import puts, colored
import progressbar

from selenium import webdriver
from selenium.webdriver.chrome.options import Options

from .common import NO_CHROME_DRIVER


def extract_zip(filename):
    """
    Uses zipfile package to extract a single zipfile
    :param filename:
    :return: new filename
    """
    try:
        file = zipfile.ZipFile(filename, 'r')
    except FileNotFoundError:
        puts(colored.red(f"{filename} Does not exist"))
        sys.exit()

    # Save the name of the new file
    new_file_name = file.namelist()[0]

    # Extract the file and make it executable
    file.extractall()

    driver_stat = os.stat(new_file_name)
    os.chmod(new_file_name, driver_stat.st_mode | stat.S_IEXEC)

    file.close()
    os.remove(filename)
    return new_file_name


def setup_selenium(driver_path, options):
    # Configures selenium to use a custom path
    driver = webdriver.Chrome(executable_path=driver_path, options=options)
    return driver


def get_webdriver():
    """
     Ensure a webdriver is available
     If Not, Download it.
    """
    cwd = os.listdir(os.getcwd())
    webdriver_regex = re.compile('chromedriver')
    web_driver = list(filter(webdriver_regex.match, cwd))

    if web_driver:
        # check if a extracted copy already exists
        if not os.path.isfile('chromedriver'):
            # Extract file
            extract_zip(web_driver[0])

        return os.getcwd() + '/chromedriver'

    else:
        # Download it according to the current machine
        webdrivers = ['https://chromedriver.storage.googleapis.com/78.0.3904.70/chromedriver_mac64.zip',
                      'https://chromedriver.storage.googleapis.com/78.0.3904.70/chromedriver_linux64.zip',
                      'https://chromedriver.storage.googleapis.com/78.0.3904.70/chromedriver_win32.zip'
                      ]
        os_platform = platform.system()
        if os_platform == 'Darwin':
            chrome_webdriver = webdrivers[0]
        elif os_platform == 'Linux':
            chrome_webdriver = webdrivers[1]
        elif os_platform == 'Windows':
            chrome_webdriver = webdrivers[2]
        else:
            raise Exception("Unknown Operating system platform")

        global total_size

        def show_progress(*res):
            global total_size
            pbar = None
            downloaded = 0
            block_num, block_size, total_size = res

            if not pbar:
                pbar = progressbar.ProgressBar(maxval=total_size)
                pbar.start()
            downloaded += block_num * block_size

            if downloaded < total_size:
                pbar.update(downloaded)
            else:
                pbar.finish()

        puts(colored.yellow("Downloading Chrome Webdriver"))
        file_name = chrome_webdriver.split('/')[-1]
        response = urlretrieve(chrome_webdriver, file_name, show_progress)

        if int(response[1].get('Content-Length')) == total_size:
            puts(colored.green(f"DONE!"))

            return os.getcwd() + '/' + extract_zip(file_name)
        else:
            puts(colored.red("An error Occurred While trying to download the driver."))
            # remove the downloaded file and exit
            os.remove(file_name)
            sys.stderr.write(NO_CHROME_DRIVER)
            sys.exit(1)
