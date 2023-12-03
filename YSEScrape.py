from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
import requests
from bs4 import BeautifulSoup

YSEpath = "https://ziggy.ucolick.org/yse/login/?next=/yse/dashboard/"

# payload = {
#     'username': "hstacey",
#     'password': "CDK700@Thacher"
# }

username = "hstacey"
password = "CDK700@Thacher"
delay = 100

driver = webdriver.Chrome()
driver.get(YSEpath)
driver.find_element(By.NAME, "username").send_keys(username)
driver.find_element(By.NAME, "password").send_keys(password)
driver.find_element(By.XPATH, '/html/body/div/div[2]/form/div[3]/div/button').click()
# table = driver.find_element(By.CLASS_NAME, 'table table-bordered table-hover')

try:
    myElem = WebDriverWait(driver, delay).until(EC.presence_of_element_located((By.CLASS_NAME, 'table table-bordered table-hover')))
    print("Page is ready!")
except TimeoutException:
    print ("Loading took too much time!")
    
# url = "https://ziggy.ucolick.org/yse/dashboard/"
# r = requests.get(url)
# parser = BeautifulSoup(r.content, "html.parser")
# table = parser.find("table")

# import mechanize
# from bs4 import BeautifulSoup
# import urllib3
# import http.cookiejar

# cj = http.cookiejar.CookieJar()
# br = mechanize.Browser()
# br.set_cookiejar(cj)
# br.open(YSEpath)













