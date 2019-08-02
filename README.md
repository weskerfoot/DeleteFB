## Why?

I needed a simple and reliable way to delete Facebook posts. There are
third-party apps that claim to do this, but they all require handing over your
credentials, or are unreliable in other ways. Since this uses Selenium, it is
more reliable, as it uses your real web browser, and it is less likely Facebook
will block or throttle you.

As for why you would want to do this in the first place. That is up to you.
Personally I wanted a way to delete most of my content on Facebook without
deleting my account.

## Will this *really* delete posts?
I can make no guarantees that Facebook doesn't store the data somewhere forever
in cold storage. However this tool is intended more as a way to clean up your
online presence and not have to worry about what you wrote from years ago.
Personally, I did this so I would feel less attached to my Facebook profile
(and hence feel the need to use it less).

## Installation
You have several options to run it.
1) Install from PyPI with `pip3 install --user delete-facebook-posts` (recommended)
2) Clone this repo and run `pip3 install --user .` or do `pip3 install --user
git+https://github.com/weskerfoot/DeleteFB.git`
3) Set up a Python virtualenv, activate it, and run `pip3 install -r requirements.txt`, then you can just run `python -m deletefb.deletefb` in the DeleteFB directory.

## How To Use It

* Make sure that you have a recent version of Python 3.x installed (preferably
  3.6 or greater)
* Make sure that you have Google Chrome installed and that it is up to date
* Also install the chromedriver for Selenium. See [here](https://sites.google.com/a/chromium.org/chromedriver/home) for an explanation of what the chromedriver does.
  * On Linux, it will be called something like `chromium-chromedriver` or just
    `chromium`.
  * On MacOS, it will be available via brew, with the following commands:

    ```
    brew tap homebrew/cask;
    brew cask install chromedriver
    ```

* Run `deletefb -E 'youremail@example.org' -P 'yourfacebookpassword' -U 'https://www.facebook.com/your.profile.url'`
* The script will log into your Facebook account, go to your profile page, and
  start deleting posts. If it cannot delete something, then it will "hide" it
  from your timeline instead.
* Be patient as it will take a very long time, but it will eventually clear
  everything. You may safely minimize the chrome window without breaking it.

## Login
* The tool will log in using the credentials passed to it. It will wait until the page `https://www.facebook.com/` is loaded in order to avoid any issues with logging in. If you pass a 2FA token explicitly with the `-F` option, then it will try to enter that for you. If there are any issues, it simply pauses indefinitely to allow the user to resolve the problems, and then continues execution.

## 2FA
* It is recommended that you disable Two-Factor Authentication temporarily
  while you are running the script, in order to get the best experience.

* If you run into issues with Facebook complaining about your browser,
  currently the only workaround is to manually click through them.

* If you do have 2-Factor Auth configured then the script will pause for 35
  seconds to allow you to enter your code and log in.

* You may also pass in a code by using the `-F` argument, e.g. `-F 111111`.

## Delete By Year
* The tool supports passing the `--year` flag in order to delete/archive by year. E.g. `-Y 2010` would only affect posts from 2010.

## Archival
* The tool will archive everything being deleted by default in `.log` files.
  Currently they are simply stored as JSON objects for each line in the log. It
  will archive the content, and a timestamp if it is available. You may disable
  this feature by using `--no-archive`.

## Headless mode
* The tool supports running Chrome in headless mode with the `--headless`
  option, which may be preferable if you plan on running it in the background.

## Bugs

If it stops working or otherwise crashes, delete the latest post manually and
start it again after waiting a minute. I make no guarantees that it will work
perfectly for every profile. Please file an issue if you run into any problems.
