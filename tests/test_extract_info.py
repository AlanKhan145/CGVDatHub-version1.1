from extractor.cgv_extractor import *
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from extractor.motchill_extractor import *

service = Service()
driver = webdriver.Chrome(service=service)
extractor = MotchillExtractor(driver, "https://motchilli.fm/phim/cha-gia")
film = extractor.extract_info()
print(film)
extractor.quit()