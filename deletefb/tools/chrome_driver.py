from ..exceptions import UnknownOSException, ChromeError
from .common import NO_CHROME_DRIVER
from clint.textui import puts, colored
from selenium import webdriver
from shutil import which
from subprocess import check_output
from urllib.request import urlretrieve
from appdirs import AppDirs
from ..version import version
from os.path import exists

import os, sys, stat, platform
import progressbar
import re
import zipfile
import requests
import pathlib

cache_dir = AppDirs("DeleteFB", version=version).user_cache_dir

try:
    pathlib.Path(cache_dir).mkdir(parents=True, exist_ok=True)
except FileExistsError:
    pass

def extract_zip(filename, chrome_maj_version):
    """
    Uses zipfile package to extract a single zipfile
    :param filename:
    :return: new filename
    """

    # Remove any leftover unversioned chromedriver
    try:
        os.remove(f"{cache_dir}/chromedriver")
    except FileNotFoundError:
        pass

    try:
        _file = zipfile.ZipFile(filename, 'r')
    except FileNotFoundError:
        puts(colored.red(f"{filename} Does not exist"))
        sys.exit(1)

    # Save the name of the new file
    new_file_name = f"{cache_dir}/{_file.namelist()[0] + chrome_maj_version}"

    # Extract the file and make it executable
    _file.extractall(path=cache_dir)

    # Rename the filename to a versioned one
    os.rename(f"{cache_dir}/chromedriver", f"{cache_dir}/chromedriver{chrome_maj_version}")

    driver_stat = os.stat(new_file_name)
    os.chmod(new_file_name, driver_stat.st_mode | stat.S_IEXEC)

    _file.close()
    os.remove(filename)
    return new_file_name


def setup_selenium(options, chrome_binary_path):
    # Configures selenium to use a custom path
    driver_path = get_webdriver(chrome_binary_path)

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

    return version, chrome_drivers.get(platform_string).format(requests.get(latest_release_url).text)

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

    # Download it according to the current machine
    chrome_maj_version, chrome_webdriver = construct_driver_url(chrome_binary_path)

    driver_path = f"{cache_dir}/chromedriver{chrome_maj_version}"

    if exists(driver_path):
        return driver_path

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
    file_name = f"{cache_dir}/{chrome_webdriver.split('/')[-1]}"
    response = urlretrieve(chrome_webdriver, file_name, show_progress)

    if int(response[1].get("Content-Length")) == total_size:
        puts(colored.green("Completed downloading the Chrome Driver."))

        return extract_zip(file_name, chrome_maj_version)

    else:
        puts(colored.red("An error Occurred While trying to download the driver."))
        # remove the downloaded file and exit
        os.remove(file_name)
        sys.stderr.write(NO_CHROME_DRIVER)
        sys.exit(1)
