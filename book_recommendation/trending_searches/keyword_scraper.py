from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import time


def get_kyobo_hot_keywords():
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")

    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

    try:
        driver.get("https://www.kyobobook.co.kr/")
        time.sleep(2)
        driver.find_element(By.CLASS_NAME, "ip_gnb_search").click()
        time.sleep(2)

        elements = driver.find_elements(By.CSS_SELECTOR, ".hot_keyword_item .keyword")
        keywords = [e.text.strip() for e in elements if e.text.strip()]
        return keywords
    finally:
        driver.quit()
