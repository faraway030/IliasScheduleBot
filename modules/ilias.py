#!/usr/bin/python3
# ilias.py

# Copyright (c) 2021, Steven Bruck

from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import time
import filecmp
import os
import logging


class Schedule(object):
    def __init__(self, username, password, filename, timeout, url, step1, step2):
        #   Config
        self.username = username
        self.pwd = password
        self.filename = filename
        self.timeout = timeout
        self.url = url
        self.step1 = step1
        self.step2 = step2

        self.appdir = os.path.abspath(
            os.path.join(os.path.dirname(__file__), '..'))
        # TODO: Fix crosslink error when setting tmp-dir outside of /bot/data
        self.tempdir = self.appdir + "/data/tmp"
        self.tempFile = self.tempdir + "/" + filename
        self.file = self.appdir + "/data/" + filename

        # Configure browser
        self.fp = webdriver.FirefoxProfile()
        self.fp.set_preference("browser.download.folderList", 2)
        self.fp.set_preference(
            "browser.download.manager.showWhenStarting", False)
        self.fp.set_preference("browser.download.dir", self.tempdir)
        self.fp.set_preference(
            "browser.helperApps.neverAsk.saveToDisk", "application/pdf")
        self.fp.set_preference("pdfjs.disabled", True)
        self.options = Options()
        self.options.binary_location = '/usr/bin/firefox'
        self.options.headless = True

        # Init logger
        logging.basicConfig(
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
        self.logger = logging.getLogger("ILIAS")

    def compare(self):
        # Compare files, return result and replace pdf on update
        if not os.path.exists(self.file):
            os.rename(self.tempFile, self.file)
            return False
        elif filecmp.cmp(self.file, self.tempFile):
            os.remove(self.tempFile)
            return True
        else:
            os.remove(self.file)
            os.rename(self.tempFile, self.file)
            return False

    def update(self):
        # Init browser instance and open login page
        browser = webdriver.Firefox(
            firefox_profile=self.fp, firefox_options=self.options)
        _step = WebDriverWait(browser, self.timeout)

        try:
            # open login page
            browser.get(self.url)

            # login
            login_attempt = _step.until(EC.presence_of_element_located(
                (By.XPATH, "//input[@type='submit']")))

            browser.find_element_by_id("username").send_keys(self.username)
            browser.find_element_by_id("password").send_keys(self.pwd)

            login_attempt.click()

            # move to schedule page
            _step.until(EC.presence_of_element_located(
                (By.LINK_TEXT, self.step1))).click()

            # download pdf
            _step.until(EC.presence_of_element_located(
                (By.LINK_TEXT, self.step2))).click()

            # wait for download to complete
            while not os.path.exists(self.tempFile):
                time.sleep(1)
        except Exception as e:
            self.logger.error(e)
        finally:
            # close the browser
            browser.close()

        #   return if update is available
        if not self.compare():
            self.logger.info("New schedule is available")
            return True
        else:
            self.logger.info("Schedule is still up to date")
            return False
