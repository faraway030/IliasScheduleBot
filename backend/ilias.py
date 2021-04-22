#!/usr/bin/python3
# ilias.py

'''
Copyright (C) 2021  Steven Bruck

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <https://www.gnu.org/licenses/>.
'''

from backend.handler import BotHandler
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import time
import filecmp
import os
import logging


class Ilias(BotHandler):
    def __init__(self, token, username, password, filename, timeout, url, step1, step2):
        super(Ilias, self).__init__(token, filename)

        #   Config
        self.__username = username
        self.__pwd = password
        self.__timeout = timeout
        self.__url = url
        self.__step1 = step1
        self.__step2 = step2

        self.__appdir = os.path.abspath(
            os.path.join(os.path.dirname(__file__), '..'))
        # TODO: Fix crosslink error when setting tmp-dir outside of /bot/data
        self.__tempdir = self.__appdir + "/data/tmp"
        self.__tempFile = self.__tempdir + "/" + filename
        self.__file = self.__appdir + "/data/" + filename

        # Firefox profile
        self.__fp = webdriver.FirefoxProfile()
        self.__fp.set_preference("browser.download.folderList", 2)
        self.__fp.set_preference(
            "browser.download.manager.showWhenStarting", False)
        self.__fp.set_preference("browser.download.dir", self.__tempdir)
        self.__fp.set_preference(
            "browser.helperApps.neverAsk.saveToDisk", "application/pdf")
        self.__fp.set_preference("pdfjs.disabled", True)

        # Firefox options
        self.__options = Options()
        self.__options.binary_location = '/usr/bin/firefox'
        self.__options.headless = True

        # Init logger
        logging.basicConfig(
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
        self.logger = logging.getLogger("ILIAS")

    def __compare(self):
        # Compare files, return result and replace pdf on update
        if not os.path.exists(self.__file):
            os.rename(self.__tempFile, self.__file)
            return False
        elif filecmp.cmp(self.__file, self.__tempFile):
            os.remove(self.__tempFile)
            return True
        else:
            os.remove(self.__file)
            os.rename(self.__tempFile, self.__file)
            return False

    def update(self):
        # Init browser instance
        browser = webdriver.Firefox(
            firefox_profile=self.__fp, firefox_options=self.__options)
        _step = WebDriverWait(browser, self.__timeout)

        try:
            # open login page
            browser.get(self.__url)

            # login
            login_attempt = _step.until(EC.presence_of_element_located(
                (By.XPATH, "//input[@type='submit']")))

            browser.find_element_by_id("username").send_keys(self.__username)
            browser.find_element_by_id("password").send_keys(self.__pwd)

            login_attempt.click()

            # move to schedule page
            _step.until(EC.presence_of_element_located(
                (By.LINK_TEXT, self.__step1))).click()

            # download pdf
            _step.until(EC.presence_of_element_located(
                (By.LINK_TEXT, self.__step2))).click()

            # wait for download to complete
            while not os.path.exists(self.__tempFile):
                time.sleep(1)
        except Exception as e:
            self.logger.error(e)
        finally:
            # close the browser
            browser.close()

        #   return if update is available
        if not self.__compare():
            self.logger.info("New schedule is available")
            return True
        else:
            self.logger.info("Schedule is still up to date")
            return False
