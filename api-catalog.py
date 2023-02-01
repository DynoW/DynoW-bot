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
import pyautogui

with open("catalog.json", "r") as r:
    catalog = json.load(r)
with open("materii.json", "r") as r:
    materii = json.load(r)
with open("secret.json", "r") as s:
    secret = json.load(s)

options = Options()
options.add_argument("--headless")
options.add_argument("user-data-dir=D:\\Documents HDD\\VSC\\bot-nike\\cache")
options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
                     + "AppleWebKit/537.36 (KHTML, like Gecko)"
                     + "Chrome/87.0.4280.141 Safari/537.36")

driver = webdriver.Chrome("chromedriver", options=options)
driver.implicitly_wait(10)

driver.get("https://www.24edu.ro/Catalog")
time.sleep(1.5)

if driver.current_url.startswith("https://www.24edu.ro/Cont/Autentificare?ReturnUrl=%2FCatalog"):
    email = driver.find_element(By.ID, "UserName")
    email.send_keys(secret["UserName"])
    email.send_keys(Keys.RETURN)
    password = driver.find_element(By.ID, "Password")
    password.send_keys(secret["Password"])
    WebDriverWait(driver, 5).until(EC.frame_to_be_available_and_switch_to_it(
        (By.CSS_SELECTOR, "iframe[name^='a-'][src^='https://www.google.com/recaptcha/api2/anchor?']")))
    WebDriverWait(driver, 5).until(
        EC.element_to_be_clickable((By.XPATH, "//span[@id='recaptcha-anchor']"))).click()
    driver.maximize_window()
    time.sleep(1)
    if EC.element_to_be_clickable((By.XPATH, "//table")):
        pyautogui.click(979, 916)
        time.sleep(3)
        pyautogui.click(939, 692)
    else:
        pyautogui.click(939, 692)
    time.sleep(30)
    print("Mere!")

if driver.current_url.startswith("https://www.24edu.ro/Catalog"):
    for elev in catalog:
        driver.get(
            f"""https://www.24edu.ro/Elev/Situatie/NivelMateriiMorrisBarData?elevId={elev['elevId']}&anScolarId=2022&semestruScolarId=19""")
        out = driver.find_element(By.TAG_NAME, "pre").text
        print(out)
        elev['Medii'] = json.loads(out)
        for materie in materii:
            driver.get(
                f"""https://www.24edu.ro/Elev/Situatie/EvolutieFlotData?elevId={elev['elevId']}&materieId={materie['materieId']}&anScolarId=2022&semestruScolarId=19""")
            out = driver.find_element(By.TAG_NAME, "pre").text
            print(materie)
            elev['Materii'][materie['materieIndex']]['Despre'] = []
            print(elev['Materii'][materie['materieIndex']]['Despre'])
            elev['Materii'][materie['materieIndex']]['Despre'].append(json.loads(out))
            print(materie['materieIndex'])
with open("catalog.json", "w") as r:
    json.dump(catalog, r, indent=2)
