#import speech_recognition as sr
#print(len(sr.Microphone.list_microphone_names()))

from speech_recognition import *
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time, pathlib, pickle, pprint, os, shutil, pyautogui
from csv import DictReader

file_path = str(pathlib.Path(__file__).parent.absolute())
file_path = file_path.replace(file_path[0], file_path[0].upper())

movie = "civil war"

chrome_browser.find_element_by_xpath('//*[@id="searchField"]').send_keys(movie)
time.sleep(2)
chrome_browser.find_element_by_xpath('//*[@id="app"]/div/div/div[1]/div[1]/div/div[2]/div/div[4]/div[1]/i').click()
time.sleep(4)
chrome_browser.find_element_by_xpath('//*[@id="app"]/div/div/div[1]/div[2]/div/div/div/div/div[2]/div[1]/div/div/article/a/div[2]/div[4]').click()
time.sleep(4)
chrome_browser.find_element_by_xpath('//*[@id="app"]/div/div/div[1]/div[2]/div[1]/div/div[1]/div[8]/div/div[4]/div[2]/div[3]/div[4]/div').click()

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
options = Options()
options.add_argument("--user-data-dir=C:/Users/ABI/Desktop/BE CSE/Projects/Virtual Assistant/UserData")
options.page_load_strategy = 'normal'
driver = webdriver.Chrome(file_path + '\Chrome driver Selenium\chromedriver.exe', options=options)
driver.get("https://www.hotstar.com/in")
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
options = Options()
options.add_argument("--user-data-dir=C:/Users/ABI/Desktop/BE CSE/Projects/Virtual Assistant/UserData")
options.page_load_strategy = 'normal'
driver = webdriver.Chrome(file_path + '\Chrome driver Selenium\chromedriver.exe', options=options)
driver.get("https://www.primevideo.com/")

time.sleep(40)

driver.get("https://www.hotstar.com/in")
'''
#print(pyautogui.getAllTitles())
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time
# creating chrome instance
opt = Options()
#opt.add_argument('--disable-blink-features=AutomationControlled')
opt.add_argument('--start-maximized')
opt.add_experimental_option("prefs", {
  
    "profile.default_content_setting_values.media_stream_mic": 1,
    "profile.default_content_setting_values.media_stream_camera": 1,
    "profile.default_content_setting_values.geolocation": 0,
    "profile.default_content_setting_values.notifications": 1
})
driver = webdriver.Chrome(options=opt)
driver.get("https://mail.google.com/mail/u/1/#inbox")
'''