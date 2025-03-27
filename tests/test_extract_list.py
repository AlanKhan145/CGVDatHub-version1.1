from extractor.cgv_extractor import *
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from extractor.motchill_extractor import *

NOW_SHOWING_URL = "https://motchilli.fm/danh-sach/phim-chieu-rap"
service = Service()
driver = webdriver.Chrome(service=service)
extractor = MotchillExtractor(driver, NOW_SHOWING_URL)
films = extractor.extract_list_film()
for film in films:
    print(film)
extractor.quit()