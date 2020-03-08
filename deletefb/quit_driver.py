import os

def quit_driver_and_reap_children(driver):
    """
    Reaps child processes by waiting until they exit.
    """
    driver.quit()
    try:
        pid = True
        while pid:
            pid = os.waitpid(-1, os.WNOHANG)
    except ChildProcessError:
        pass
