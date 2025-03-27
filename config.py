"""
Cấu hình kết nối MongoDB và các thông số liên quan đến việc thu thập dữ liệu phim từ CGV.
"""

POSTGRES_URL = "mongodb+srv://CgvHub:o@cluster0.ktuns.mongodb.net/"
DATABASE_NAME = "cgv_movies_2"

# Tên collection trong MongoDB
FILM_COLLECTION_NAME = "films"
# URL của các trang phim
NOW_SHOWING_URL = "https://www.cgv.vn/default/movies/now-showing.html"
COMING_SOON_URL = "https://www.cgv.vn/default/movies/coming-soon-1.html"
# Thời gian chờ (giây) giữa các lần thu thập dữ liệu
WAIT_TIME = 2