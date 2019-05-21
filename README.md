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

## How To Use

* Make sure that you have Google Chrome installed and that it is up to date
* Also install the chromedriver for Selenium. See [here](https://sites.google.com/a/chromium.org/chromedriver/downloads). On Arch Linux you can find this in the `chromium` package, and on Ubuntu it is `chromium-chromedriver`.
* `pip3 install --user delete-facebook-posts`
* `deletefb -E "youremail@example.org" -P "yourfacebookpassword" -U "https://www.facebook.com/your.profile.url"`
* The script will log into your Facebook account, go to your profile page, and
  start deleting posts. If it cannot delete something, then it will "hide" it
  from your timeline instead.
* Be patient as it will take a very long time, but it will eventually clear
  everything. You may safely minimize the chrome window without breaking it.

## 2FA
* If you have 2-Factor Auth configured then the script will pause for 20
  seconds to allow you to enter your code and log in.

## Headless mode
* The tool supports running Chrome in headless mode with the `--headless`
  option, which may be preferable if you plan on running it in the background.

## How To Install Python

### MacOS
See [this link](https://docs.python-guide.org/starting/install3/osx/) for
instructions on installing with Brew.

### Linux
Use your native package manager

### Windows
See [this link](https://www.howtogeek.com/197947/how-to-install-python-on-windows/), but I make no guarantees that Selenium will actually work as I have not tested it.


### Bugs

If it stops working or otherwise crashes, delete the latest post manually and
start it again after waiting a minute. I make no guarantees that it will work
perfectly for every profile. Please file an issue if you run into any problems.
