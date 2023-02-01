from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import json

with open("catalog.json", "r") as r:
    catalog = json.load(r)
with open("materii.json", "r") as r:
    materii = json.load(r)
with open("secret.json", "r") as s:
    secret = json.load(s)

options = Options()
options.add_argument("--headless")
options.add_argument('--no-sandbox')
options.add_argument("user-data-dir=D:\\Documents HDD\\VSC\\bot-nike\\cache")
options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
                     + "AppleWebKit/537.36 (KHTML, like Gecko)"
                     + "Chrome/87.0.4280.141 Safari/537.36")

driver = webdriver.Chrome(options=options)
driver.implicitly_wait(10)

driver.get("https://www.24edu.ro/Catalog")
time.sleep(1.5)
print(driver.title)
