from ..exceptions import UnknownOSException, ChromeError
from .common import NO_CHROME_DRIVER
from clint.textui import puts, colored
from selenium import webdriver
from shutil import which
from subprocess import check_output
from urllib.request import urlretrieve

import os, sys, stat, platform
import progressbar
import re
import zipfile
import requests

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

def parse_version(output):
    """
    Attempt to extract version number from chrome version string.
    """
    return [c for c in re.split('([0-9]+)\.?', output.decode("utf-8")) if all(d.isdigit() for d in c) and c][0]

def get_chrome_version(chrome_binary_path=None):
    """
    Extract the chrome major version.
    """
    driver_locations = [which(loc) for loc in ["google-chrome", "google-chrome-stable", "chromium", "chrome.exe"]]

    for location in driver_locations:
        print(location)
        if location:
            return parse_version(check_output([location, "--version"]).strip())
    return None

def construct_driver_url(chrome_binary_path=None):
    """
    Construct a URL to download the Chrome Driver.
    """

    platform_string = platform.system()
    chrome_drivers = {
        "Windows" : "https://chromedriver.storage.googleapis.com/{0}/chromedriver_win32.zip",
        "Darwin" : "https://chromedriver.storage.googleapis.com/{0}/chromedriver_mac64.zip",
        "Linux" : "https://chromedriver.storage.googleapis.com/{0}/chromedriver_linux64.zip"
    }

    version = get_chrome_version()

    if version is None:
        raise ChromeError("Chrome version not found")

    latest_release_url = "https://chromedriver.storage.googleapis.com/LATEST_RELEASE_{0}".format(version)

    return chrome_drivers.get(platform_string).format(requests.get(latest_release_url).text)

    # First, construct a LATEST_RELEASE URL using Chrome's major version number.
    # For example, with Chrome version 73.0.3683.86, use URL "https://chromedriver.storage.googleapis.com/LATEST_RELEASE_73".
    # Try to download a small file from this URL. If it successful, the file contains the ChromeDriver version to use.
    # If the above step failed, reduce the Chrome major version by 1 and try again.
    # For example, with Chrome version 75.0.3745.4, use URL "https://chromedriver.storage.googleapis.com/LATEST_RELEASE_74"
    #  to download a small file, which contains the ChromeDriver version to use.
    # You can also use ChromeDriver Canary build.

def get_webdriver(chrome_binary_path):
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

        chrome_webdriver = construct_driver_url(chrome_binary_path)

        if not chrome_webdriver:
            raise UnknownOSException("Unknown Operating system platform")

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

        if int(response[1].get("Content-Length")) == total_size:
            puts(colored.green("Completed downloading the Chrome Driver."))

            return "{0}/{1}".format(os.getcwd(), extract_zip(file_name))

        else:
            puts(colored.red("An error Occurred While trying to download the driver."))
            # remove the downloaded file and exit
            os.remove(file_name)
            sys.stderr.write(NO_CHROME_DRIVER)
            sys.exit(1)
