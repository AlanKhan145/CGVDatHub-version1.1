from selenium import webdriver
from selenium.webdriver.chrome.service import Service

from extractor.motchill_extractor import MotchillExtractor
from db.database import Base, SessionLocal, engine
from db.models import Film
from db.crud import get_all_films

# Khởi tạo database
Base.metadata.create_all(bind=engine)
db = SessionLocal()

# Định nghĩa URL
test_url = "https://motchilli.fm/danh-sach/phim-chieu-rap"

# Khởi tạo trình duyệt Chrome
service = Service()  # Nếu cần đường dẫn cụ thể: Service("path/to/chromedriver")
driver = webdriver.Chrome(service=service)

try:
    # Khởi tạo extractor và lấy danh sách phim
    extractor = MotchillExtractor(driver, test_url)
    extractor.extract_list_films(db)

    # Lấy danh sách phim từ database và in ra
    films_list = get_all_films(db)
    for film in films_list:
        print(film)
finally:
    driver.quit()
    db.close()
