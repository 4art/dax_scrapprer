from selenium import webdriver
from selenium.common import TimeoutException
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time


class Scraper:
    def __init__(self):
        self.init_server()

    def init_server(self):
        self.url = "https://www.unternehmensregister.de/ureg/"
        options = webdriver.ChromeOptions()
        prefs = {"download.default_directory": "/tmp/reports/daxes"}
        options.add_experimental_option("prefs", prefs)
        self.driver = webdriver.Chrome(chrome_options=options)
        self.driver.get(self.url)
        cookies_accept_button = self.driver.find_element(By.ID, "cc_all")
        if cookies_accept_button:
            cookies_accept_button.click()

    def download_company(self, company_name):
        search_input = self.driver.find_element(By.ID, "globalSearchForm:extendedResearchCompanyName")
        search_input.clear()
        search_input.send_keys(company_name)
        delay = 0.3
        if self.wait_and_click(By.ID, "globalSearchForm:btnExecuteSearchOld"): return
        if self.wait_and_click(By.PARTIAL_LINK_TEXT, "Registerinformationen des Registergerichts"): return
        if self.wait_and_click(By.PARTIAL_LINK_TEXT, "Registerinformationen anzeigen"): return
        if self.wait_and_click(By.PARTIAL_LINK_TEXT, "AD"): return
        if self.wait_and_click(By.PARTIAL_LINK_TEXT, "Dokumentenkorb ansehen"): return
        time.sleep(delay)
        self.driver.find_elements(By.CSS_SELECTOR, "input.btn.btn-green")[1].click()
        time.sleep(delay)
        self.driver.find_elements(By.CSS_SELECTOR, "input.btn.btn-green")[1].click()
        if self.wait_and_click(By.PARTIAL_LINK_TEXT, "Zum Dokumentenkorb"): return
        if self.wait_and_click(By.PARTIAL_LINK_TEXT, "Dokument abrufen"): return
        if self.wait_and_click(By.CSS_SELECTOR, "a.logo"): return

        time.sleep(delay)

    def wait_and_click(self, by, value, delay=10):
        err = False
        try:
            WebDriverWait(self.driver, delay).until(
                EC.presence_of_element_located((by, value)))
        except TimeoutException:
            print("Timed out waiting for page to load")
            err = True
        finally:
            if err:
                self.close()
                self.init_server()
            else:
                self.driver.find_element(by, value).click()
            return err

    def close(self):
        self.driver.close()
