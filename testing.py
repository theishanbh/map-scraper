from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

driver = webdriver.Chrome("chromedriver.exe")
# driver.get('https://www.google.com/maps')
driver.get('https://www.google.com/maps?hl=en')
# 