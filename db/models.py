from db.database import Base
from sqlalchemy import Column, Integer, String, Text, Boolean

class Film(Base):
    __tablename__ = 'motchill'

    title = Column(String, primary_key=True, nullable=False, unique=True)  # Tiêu đề phim là khóa chính
    status = Column(String, nullable=True)
    director = Column(String, nullable=True)
    duration = Column(String, nullable=True)
    episodes = Column(String, nullable=True)  # Số tập
    language = Column(String, nullable=True)
    release_year = Column(Integer, nullable=True)  # Năm phát hành
    country = Column(String, nullable=True)
    genre = Column(String, nullable=True)
    actors = Column(Text, nullable=True)  # Danh sách diễn viên
    description = Column(Text, nullable=True)  # Mô tả phim
    poster = Column(String, nullable=True)  # Link ảnh poster
    is_active = Column(Boolean, default=True)  # Phim còn hoạt động không

    def __init__(self, **kwargs):
        """Khởi tạo Film từ dictionary"""
        for key, value in kwargs.items():
            if hasattr(self, key):  # Chỉ gán giá trị nếu thuộc tính tồn tại
                setattr(self, key, value)

    def print_info(self):
        """In ra thông tin của bộ phim"""
        print(f"Title: {self.title}")
        print(f"Status: {self.status}")
        print(f"Director: {self.director}")
        print(f"Duration: {self.duration}")
        print(f"Episodes: {self.episodes}")
        print(f"Language: {self.language}")
        print(f"Release Year: {self.release_year}")
        print(f"Country: {self.country}")
        print(f"Genre: {self.genre}")
        print(f"Actors: {self.actors}")
        print(f"Description: {self.description}")
        print(f"Poster: {self.poster}")
        print(f"Active: {'Yes' if self.is_active else 'No'}")