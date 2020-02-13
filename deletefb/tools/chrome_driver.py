from ..exceptions import UnknownOSException
from .common import NO_CHROME_DRIVER
from clint.textui import puts, colored
from selenium import webdriver

import os, sys, stat, platform
import progressbar
import re
import zipfile
import requests


chrome_drivers = {
    "Windows" : "https://chromedriver.storage.googleapis.com/{0}/chromedriver_win32.zip",
    "Darwin" : "https://chromedriver.storage.googleapis.com/{0}/chromedriver_mac64.zip",
    "Linux" : "https://chromedriver.storage.googleapis.com/{0}/chromedriver_linux64.zip"
}

def extract_zip(filename):
    """
    Uses zipfile package to extract a single zipfile
    :param filename:
    :return: new filename
    """
    try:
        _file = zipfile.ZipFile(filename, 'r')
    except FileNotFoundError:
        puts(colored.red(f"{filename} Does not exist"))
        sys.exit(1)

    # Save the name of the new file
    new_file_name = _file.namelist()[0]

    # Extract the file and make it executable
    _file.extractall()

    driver_stat = os.stat(new_file_name)
    os.chmod(new_file_name, driver_stat.st_mode | stat.S_IEXEC)

    _file.close()
    os.remove(filename)
    return new_file_name


def setup_selenium(driver_path, options):
    # Configures selenium to use a custom path
    return webdriver.Chrome(executable_path=driver_path, options=options)

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

        return "{0}/chromedriver".format(os.getcwd())

    else:
        # Download it according to the current machine

        chrome_webdriver = chrome_drivers.get(platform.system(), False)
        if not chrome_webdriver:
            raise UnknownOSException("Unknown Operating system platform")

        file_name = chrome_webdriver.split('/')[-1]
        try:
            r = requests.get('https://chromedriver.storage.googleapis.com/LATEST_RELEASE')
            r.raise_for_status()
            latest_release = r.text
            puts(colored.yellow("Downloading Chrome Webdriver {0}".format(latest_release)))

            with open(file_name, 'wb') as f:
                r = requests.get(chrome_webdriver.format(latest_release), stream=True)
                r.raise_for_status()
                total_size = int(r.headers['Content-Length'])
                pbar = progressbar.ProgressBar(maxval=total_size)
                pbar.start()
                for chunk in r.iter_content(16384):
                    pbar.update(f.write(chunk))
                pbar.finish()

            puts(colored.green(f"DONE!"))
            return "{0}/{1}".format(os.getcwd(), extract_zip(file_name))
        except Exception as e:
            puts(colored.red("An error Occurred While trying to download the driver."))
            print(e)
            # remove the downloaded file and exit
            try:
                os.remove(file_name)
            except FileNotFoundError:
                pass
            sys.stderr.write(NO_CHROME_DRIVER)
            sys.exit(1)
