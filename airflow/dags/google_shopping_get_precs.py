from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from datetime import datetime
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.actions.wheel_input import ScrollOrigin
from selenium import webdriver
import time
from selenium.webdriver.support import expected_conditions as EC
import re
import pandas as pd
from typing import Literal, List, Generator
from itertools import chain


options = webdriver.ChromeOptions() 
options.add_experimental_option("excludeSwitches", ["enable-automation"])
options.add_experimental_option('useAutomationExtension', False)
options.add_argument("--start-maximized")
options.add_argument('--disable-infobars')
driver = webdriver.Chrome(options=options, executable_path=r"D:\produtoshausz\chromedriver\chromedriver.exe")

def scroll() -> None:
    driver.implicitly_wait(7)
    lenOfPage = driver.execute_script("window.scrollTo(0, document.body.scrollHeight);var lenOfPage=document.body.scrollHeight;return lenOfPage;")
    match=False
    while(match==False):
        lastCount = lenOfPage
        time.sleep(3)
        lenOfPage = driver.execute_script("window.scrollTo(0, document.body.scrollHeight);var lenOfPage=document.body.scrollHeight;return lenOfPage;")
        if lastCount==lenOfPage:
            match=True


def reader_excel():
    driver.implicitly_wait(7)
    data = pd.read_excel(r'D:\produtoshausz\google\googleshoppingurls.xlsx')
    dicts = data.to_dict('records')
    for dic in dicts:
        time.sleep(2)
        if re.search('shopping/produc',dic['URLGOOGLE'], re.IGNORECASE):
            time.sleep(2)
            google = 'https://www.google.com/'+dic['URLGOOGLE']
            driver.get(google)
            scroll()

            print(dic['NOMEPRODUTO'],dic['Marca'],dic['SKU'],dic['IDPRODUTO'],dic['EAN'])
            try:
                sellers = driver.find_elements(By.XPATH,'//*[@id="sh-osd__online-sellers-cont"]/tr/td[1]/div[1]/a')
                for seller in sellers:
                    print(seller.text)
            except:
                pass
            
            try:
                precos = driver.find_elements(By.XPATH,'//*[@id="sh-osd__online-sellers-cont"]/tr/td[4]/div/div[1]')
                for preco in precos:
                    print(preco.text)
            except:
                pass
            
            try:
                url_anuncios = driver.find_elements(By.XPATH,'//*[@id="sh-osd__online-sellers-cont"]/tr/td/div/a')
                for urls in url_anuncios:
                    print(urls.get_attribute('href'))
            except:
                pass
                
        
