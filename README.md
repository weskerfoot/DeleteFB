## How To Use

* Make sure that you have Google Chrome installed and that it is up to date
* `pip3 install --user delete-facebook-posts`
* `deletefb -E "youremail@example.org" -P "yourfacebookpassword" -U "https://www.facebook.com/your.profile.url"`
* The script will log into your Facebook account, go to your profile page, and
  start deleting posts. If it cannot delete something, then it will "hide" it
  from your timeline instead.
* Be patient as it will take a very long time, but it will eventually clear
  everything. You may safely minimize the chrome window without breaking it.

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
