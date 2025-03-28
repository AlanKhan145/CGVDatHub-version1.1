from sqlalchemy.orm import Session
from db.models import Film
# CRUD Operations

def get_film(db: Session, title: str):
    return db.query(Film).filter(Film.title == title).first()

def get_films(db: Session, skip: int = 0, limit: int = 10):
    return db.query(Film).offset(skip).limit(limit).all()

def get_all_films(db: Session):
    return db.query(Film).all()


def create_film(db: Session, film: Film):
    existing_film = db.query(Film).filter(Film.title == film.title).first()

    if existing_film:
        # Cập nhật thông tin phim nếu đã tồn tại
        for key, value in film.__dict__.items():
            if key != "_sa_instance_state" and value is not None:
                setattr(existing_film, key, value)
        db.commit()
        db.refresh(existing_film)
        return existing_film
    else:
        # Tạo phim mới nếu chưa có
        db.add(film)
        db.commit()
        db.refresh(film)
        return film
def update_film(db: Session, title: str, updates: dict):
    film = db.query(Film).filter(Film.title == title).first()
    if film:
        for key, value in updates.items():
            setattr(film, key, value)
        db.commit()
        db.refresh(film)
    return film

def delete_film(db: Session, title: str):
    film = db.query(Film).filter(Film.title == title).first()
    if film:
        db.delete(film)
        db.commit()
    return film

