import psycopg2
from psycopg2.extras import DictCursor
import logging
from config import POSTGRES_URL


def get_connection():
    """Kết nối đến PostgreSQL và trả về đối tượng connection."""
    try:
        conn = psycopg2.connect(POSTGRES_URL)
        print("Kết nối thành công đến PostgreSQL")
        return conn
    except Exception as e:
        logging.error(f"Lỗi kết nối PostgreSQL: {e}")
        return None


def save_to_database(conn, data: dict):
    """Lưu hoặc cập nhật dữ liệu phim vào PostgreSQL."""
    if not conn:
        logging.error("Không có kết nối đến database")
        return

    try:
        with conn.cursor(cursor_factory=DictCursor) as cursor:
            cursor.execute(
                """
                INSERT INTO movies (title, status, director, duration, episodes, language, 
                                   release_year, country, genre, actors, description, poster)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                ON CONFLICT (title) 
                DO UPDATE SET status = EXCLUDED.status, director = EXCLUDED.director, 
                              duration = EXCLUDED.duration, episodes = EXCLUDED.episodes, 
                              language = EXCLUDED.language, release_year = EXCLUDED.release_year, 
                              country = EXCLUDED.country, genre = EXCLUDED.genre, 
                              actors = EXCLUDED.actors, description = EXCLUDED.description, 
                              poster = EXCLUDED.poster;
                """,
                (
                    data.get("title", "Không có thông tin"),
                    data.get("status", "Không có thông tin"),
                    data.get("director", "Không có thông tin"),
                    data.get("duration", "Không có thông tin"),
                    data.get("episodes", "Không có thông tin"),
                    data.get("language", "Không có thông tin"),
                    data.get("release_year", "Không có thông tin"),
                    data.get("country", "Không có thông tin"),
                    data.get("genre", "Không có thông tin"),
                    data.get("actors", "Không có thông tin"),
                    data.get("description", "Không có thông tin"),
                    data.get("poster", "Không có thông tin")
                )
            )
            conn.commit()
            print(f"Lưu hoặc cập nhật phim: {data.get('title', 'Không có thông tin')}")
    except Exception as e:
        logging.error(f"Lỗi khi lưu dữ liệu: {e}")
        conn.rollback()
