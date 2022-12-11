from selenium import webdriver
from selenium.common import TimeoutException
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

class Scraper:
    def __init__(self):
        self.url = "https://www.unternehmensregister.de/ureg/"
        self.driver = webdriver.Firefox()
        self.driver.get(self.url)
        cookies_accept_button = self.driver.find_element(By.ID, "cc_all")
        if cookies_accept_button:
            cookies_accept_button.click()

    def download_company(self, company_name):
        search_input = self.driver.find_element(By.ID, "globalSearchForm:extendedResearchCompanyName")
        search_input.clear()
        search_input.send_keys(company_name)
        delay = 1
        time.sleep(delay)
        self.driver.find_element(By.ID, "globalSearchForm:btnExecuteSearchOld").click()
        try:
            WebDriverWait(self.driver, delay).until(EC.presence_of_element_located((By.PARTIAL_LINK_TEXT, "Registerinformationen des Registergerichts")))
        except TimeoutException:
            print("Timed out waiting for page to load")
        finally:
            print("Page loaded")
        self.driver.find_element(By.PARTIAL_LINK_TEXT, "Registerinformationen des Registergerichts").click()
        time.sleep(delay)
        self.driver.find_element(By.PARTIAL_LINK_TEXT, "Registerinformationen anzeigen").click()
        time.sleep(delay)
        self.driver.find_element(By.PARTIAL_LINK_TEXT, "AD").click()
        time.sleep(delay)
        self.driver.find_element(By.PARTIAL_LINK_TEXT, "Dokumentenkorb ansehen").click()
        time.sleep(delay)
        self.driver.find_elements(By.CSS_SELECTOR, "input.btn.btn-green")[1].click()
        time.sleep(delay)
        self.driver.find_elements(By.CSS_SELECTOR, "input.btn.btn-green")[1].click()
        time.sleep(delay)
        self.driver.find_element(By.PARTIAL_LINK_TEXT, "Zum Dokumentenkorb").click()
        time.sleep(delay)
        self.driver.find_element(By.PARTIAL_LINK_TEXT, "Dokument abrufen").click()
        time.sleep(delay)
        try:
            WebDriverWait(self.driver, delay).until(EC.presence_of_element_located((By.CSS_SELECTOR, "a.logo")))
        except TimeoutException:
            print("Timed out waiting for page to load")
        finally:
            print("Page loaded")
        self.driver.find_element(By.CSS_SELECTOR, "a.logo").click()
        self.driver.switch_to.window(self.driver.window_handles[0])
        time.sleep(delay)

    def close(self):
        self.driver.close()