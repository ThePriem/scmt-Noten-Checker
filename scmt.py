from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
import os
import logging

def wait_until_CSS_visible(driver, cssSelector):
    WebDriverWait(driver, 10).until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, cssSelector)))

def getGradesFromWebsite(usr,pwd):
    #Configure Logging:
    logging.basicConfig(format='%(levelname)s: %(asctime)s: %(message)s',
                        datefmt='%d.%m.%Y %H:%M:%S',
                        filename='info.log', 
                        encoding='utf-8', 
                        level=logging.INFO)


    driver = webdriver.Remote("http://<selenium ip>/wd/hub", DesiredCapabilities.CHROME)


    url = "https://www.eis-scmt.com/home/lib/Controller.php?oitSource=scmt_eis&oitAction=start"

    #Open Website
    driver.get(url)

    ##Login:
    driver.find_element(By.CSS_SELECTOR,"#username").send_keys(usr)
    driver.find_element(By.CSS_SELECTOR,"#password").send_keys(pwd)
    driver.find_element(By.CSS_SELECTOR,"#ctrl_245").click()

    #Go to grades:
    driver.get("https://www.eis-scmt.com/home/lib/Controller.php?oitSource=fm1004_studium.html&oitAction=noten_show")

    tableBodys = ["#teilnehmer_leistungsnachweise_form > table > tbody:nth-child(2)",
                  "#teilnehmer_leistungsnachweise_form > table > tbody:nth-child(5)",
                  "#teilnehmer_leistungsnachweise_form > table > tbody:nth-child(8)"]

    gradeList = []

    for table in tableBodys:
        tableElement = driver.find_element(By.CSS_SELECTOR,table)
        rows = tableElement.find_elements(By.TAG_NAME,"tr")
        for row in rows:
            moduleName = row.find_elements(By.TAG_NAME,"td")[0].text
            moduleArt = row.find_elements(By.TAG_NAME,"td")[1].text #Klausur oder TDR
            moduleGrade = row.find_elements(By.TAG_NAME,"td")[3].text
            
            #Skip if no grade available
            if moduleGrade == "":
                continue
            
            gradeList.append({"name":moduleName + " - " + moduleArt,"grade":moduleGrade})
            # print(moduleName)
            # print(moduleGrade)
            # print("----")

    driver.quit()

    return gradeList
 