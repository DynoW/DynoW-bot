from selenium import webdriver
# from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
# from selenium.webdriver.support.ui import WebDriverWait
# from selenium.webdriver.support import expected_conditions as EC
import time
import json

with open("catalog.json", "r") as r:
    catalog = json.load(r)
with open("materii.json", "r") as r:
    materii = json.load(r)
with open("secret.json", "r") as s:
    secret = json.load(s)

options = Options()
# options.add_extension("extension.crx")
options.add_argument("--headless")
options.add_argument("--disable-dev-shm-usage")
options.add_argument("--no-sandbox")
options.add_argument("user-data-dir=cache")

driver = webdriver.Chrome(options=options)
driver.implicitly_wait(10)

driver.get("https://www.24edu.ro/Catalog")
print("Loaded!")
time.sleep(1)
print(driver.title)

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
