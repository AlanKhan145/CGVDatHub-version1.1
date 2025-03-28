from extractor.cgv_extractor import *
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from extractor.cgv_extractor import *

service = Service()
driver = webdriver.Chrome(service=service)
extractor = CgvExtractor(driver, "https://www.cgv.vn/default/quy-nhap-trang.html")
film = extractor.extract_info()
print(film)
extractor.quit()