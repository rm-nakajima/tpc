from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select
import time
from datetime import date, timedelta, datetime
import datetime
import chromedriver_binary
import re
import csv
from bs4 import BeautifulSoup
import requests
import copy

option = Options()
option.add_argument('--incognito')
driver = webdriver.Chrome(options=option) 

##ここに対象サイトURL
target_url = 'http://www.dubairacingclub.com/race/racing-info/trakus-chart'

##一旦Googleを経由
driver.get('https://www.google.com/')

time.sleep(1)

driver.get(target_url)

c_iframe = driver.find_element_by_css_selector('.node-content iframe')
c_iframe = c_iframe.get_attribute('src')
print(c_iframe)

driver.get(c_iframe)

sam = driver.find_element_by_css_selector('#DisplayArea tbody tr:first-child')
print(sam.text)