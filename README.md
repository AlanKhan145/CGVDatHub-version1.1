# FilmDataHub

## Giới thiệu
FilmDataHub là một dự án thu thập dữ liệu từ trang web CGV, tập trung vào danh sách phim, khuyến mãi và thông tin rạp chiếu phim. Dữ liệu được crawl, trích xuất, xử lý và lưu trữ vào MongoDB để phục vụ phân tích hoặc hiển thị.

## Chức năng chính
- Crawl dữ liệu từ các website phim: phim, khuyến mãi, thông tin rạp.
- Trích xuất chi tiết: thể loại, đạo diễn, ưu đãi, hotline, lịch chiếu.
- Lưu trữ dữ liệu vào MongoDB.

## Công nghệ sử dụng
- **Python, Jupyter Notebook**: phát triển.
- **Selenium**: thu thập dữ liệu.
- **MongoDB**: lưu trữ.
- **Logging**: theo dõi lỗi.

## Cấu trúc dự án
```
├── extractor/              # Thư mục chứa các module trích xuất dữ liệu
│   ├── __pycache__/        # Cache của Python
│   ├── base_extractor.py   # Lớp trích xuất cơ bản
│   ├── cgv_extractor.py    # Trích xuất dữ liệu từ CGV
│   ├── motchill_extractor.py # Trích xuất dữ liệu từ Motchill
│
├── tests/                  # Thư mục chứa các test cases
│   ├── __pycache__/        # Cache của Python
│   ├── test.ipynb          # Notebook kiểm thử
│   ├── test_extract_info.py # Test trích xuất thông tin
│   ├── test_extract_list.py # Test trích xuất danh sách
│
├── .gitattributes          # Cấu hình Git
├── README.md               # Tài liệu dự án
├── config.py               # File cấu hình
├── database.py             # Quản lý MongoDB
├── main.py                 # Chạy crawl dữ liệu
├── requirements.txt        # Các thư viện cần thiết
```

## Cách sử dụng
1. **Cài đặt thư viện cần thiết**
   ```bash
   pip install -r requirements.txt
   ```
2. **Chạy dự án**
     ```bash
     python main.ipynb
     ```

