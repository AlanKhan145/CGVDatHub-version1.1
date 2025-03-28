from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# Thông tin PostgreSQL
POSTGRES_HOST = "localhost"
POSTGRES_PORT = "5432"
POSTGRES_DB = "motchill"
POSTGRES_USER = "postgres"
POSTGRES_PASSWORD = "o"

# Kết nối đến PostgreSQL
SQLALCHEMY_DATABASE_URL = (
    f"postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}"
    f"@{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DB}"
)
engine = create_engine(SQLALCHEMY_DATABASE_URL)

# Tạo session
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base ORM
Base = declarative_base()
