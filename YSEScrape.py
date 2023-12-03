from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By

YSEpath = "https://ziggy.ucolick.org/yse/login/?next=/yse/dashboard/"
username = "hstacey"
password = "CDK700@Thacher"
delay = 100

driver = webdriver.Chrome()
driver.get(YSEpath)
driver.find_element(By.NAME, "username").send_keys(username)
driver.find_element(By.NAME, "password").send_keys(password)
driver.find_element(By.XPATH, '/html/body/div/div[2]/form/div[3]/div/button').click()

try:
    myElem = WebDriverWait(driver, delay).until(EC.presence_of_element_located((By.CLASS_NAME, 'table table-bordered table-hover')))
    print("Page is ready!")
except TimeoutException:
    print ("Loading took too much time!")
    
table = driver.find_element(By.ID, "k2_transient_tbl")






