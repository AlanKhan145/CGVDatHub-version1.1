from database import Base, SessionLocal, engine
from sqlalchemy.orm import Session
from db.models import Film
from db.crud import create_film, get_film, update_film, get_all_films, delete_film

# Khởi tạo database nếu chưa có
Base.metadata.create_all(bind=engine)

def test_film_operations():
    # Tạo session
    db: Session = SessionLocal()

    try:
        # Bước 1: Tạo lại bảng trong database
        Base.metadata.create_all(bind=engine)
        print("✅ Đã tạo lại các bảng trong database!")

        # Bước 2: Dữ liệu phim cần thêm
        film_data = Film(
            title="Phim Cha Giả",
            status="Mới",
            director="Đạo diễn A",
            duration="95 phút",
            episodes=1,
            language="Vietsub",
            release_year=2025,
            country="Trung Quốc",
            genre="Chính kịch, Hài Hước",
            actors="Bao Bei Er, Ding Jiali, Jia Bing",
            description="Nội dung phim Cha Giả...",
            poster="https://motchilli.fm/wp-content/uploads/2025/02/cha-gia-14849-thumb.webp",
        )

        # Bước 3: Thêm phim vào database
        new_film = create_film(db, film_data)
        print(f" Đã thêm phim: {new_film.title}")

        # Bước 4: Cập nhật thông tin phim
        updated_film_data = {"status": "Đã phát sóng"}
        updated_film = update_film(db, new_film.title, updated_film_data)
        print(f" Đã cập nhật phim: {updated_film.title} với status {updated_film.status}")

        # Bước 5: Kiểm tra lại thông tin phim đã cập nhật
        film_from_db = get_film(db, new_film.title)
        print(f" Phim từ database: {film_from_db.title} (Status: {film_from_db.status})")

        # Bước 6: Lấy toàn bộ danh sách phim
        all_films = get_all_films(db)
        print(f" Danh sách phim hiện tại: {[film.title for film in all_films]}")

        # Bước 7: Xóa phim vừa thêm
        delete_film(db, new_film.title)
        print(f" Đã xóa phim {new_film.title} khỏi database.")

        # Bước 8: Xóa tất cả các bảng trong database
        Base.metadata.drop_all(bind=engine)
        print(" Đã xóa tất cả các bảng trong database!")

    except Exception as e:
        print(f" Lỗi: {e}")

    finally:
        # Đóng session
        db.close()

# Gọi hàm kiểm tra
test_film_operations()
