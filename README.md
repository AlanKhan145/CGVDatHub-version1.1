# Film Data Hub

## Giới thiệu
Film Data Hub là một dự án thu thập và xử lý dữ liệu từ trang web CGV và MotChill, tập trung vào danh sách phim, khuyến mãi và thông tin rạp chiếu. Dữ liệu được crawl, trích xuất và lưu trữ vào **PostgreSQL**, sử dụng **SQLAlchemy** để tự động tạo cơ sở dữ liệu theo mô hình đối tượng.

Dự án được phát triển theo hướng **lập trình hướng đối tượng (OOP)**, với **base_extractor** là lớp cơ sở cho các bộ thu thập dữ liệu.

## Chức năng chính
- **Crawl dữ liệu**: Thu thập thông tin về phim, khuyến mãi và rạp chiếu từ nhiều nguồn.
- **Trích xuất chi tiết**: Gồm thể loại phim, đạo diễn, ưu đãi, hotline, lịch chiếu.
- **Lưu trữ dữ liệu**: Lưu vào **PostgreSQL**, sử dụng **SQLAlchemy ORM** để tương tác với cơ sở dữ liệu.

## Công nghệ sử dụng
- **Python**
- **Jupyter Notebook**
- **Selenium**
- **SQLAlchemy**
- **Psycopg2**
- **PostgreSQL**

## Cấu trúc dự án
```
FilmDataHub/
|-- db/                 # Quản lý cơ sở dữ liệu
|   |-- __init__.py
|   |-- crud.py         # Các thao tác CRUD với PostgreSQL
|   |-- database.py     # Kết nối với cơ sở dữ liệu
|   |-- models.py       # Định nghĩa mô hình dữ liệu
|   |-- test_connections.py  # Kiểm thử kết nối cơ sở dữ liệu
|
|-- extractor/          # Chứa các module trích xuất dữ liệu
|   |-- __init__.py
|   |-- base_extractor.py       # Lớp cơ sở cho bộ thu thập dữ liệu
|   |-- cgv_extractor.py        # Bộ thu thập dữ liệu CGV
|   |-- motchill_extractor.py   # Bộ thu thập dữ liệu MotChill
|
|-- config.py           # Cấu hình dự án
|-- main.ipynb          # File chạy chính của dự án
|-- requirements.txt    # Danh sách các thư viện cần cài đặt
|-- README.md           # Tài liệu hướng dẫn dự án
```

## Hướng dẫn sử dụng
1. **Cài đặt các thư viện cần thiết**
   ```sh
   pip install -r requirements.txt
   ```
2. **Khởi tạo cơ sở dữ liệu PostgreSQL**
   - Cấu hình thông tin kết nối trong `config.py`
   - Chạy lệnh sau để tạo bảng trong cơ sở dữ liệu:
     ```sh
     python db/models.py
     ```
3. **Chạy dự án**
   ```sh
   python main.ipynb
   ```

