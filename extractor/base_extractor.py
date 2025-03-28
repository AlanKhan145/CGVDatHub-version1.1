import logging
import os
import sys
import time
from typing import Any, Dict, List

from selenium.common.exceptions import NoSuchElementException, WebDriverException
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver
from sqlalchemy.orm import Session

from config import WAIT_TIME
import sys
import os
from db.crud import create_film
from db.models import Film


class Extractor:
    """
    Lớp trích xuất dữ liệu từ trang web bằng Selenium.
    """

    def __init__(self, driver: WebDriver, url: str):
        """
        Khởi tạo đối tượng Extractor.

        Args:
            driver (WebDriver): Trình điều khiển trình duyệt Selenium.
            url (str): URL của trang web cần trích xuất dữ liệu.
        """
        self.driver = driver
        self.driver.get(url)
        time.sleep(WAIT_TIME)

    def load_page(self, url: str) -> None:
        """
        Chuyển hướng trình duyệt đến URL mới.

        Args:
            url (str): URL của trang web mới.
        """
        self.driver.get(url)
        time.sleep(WAIT_TIME)

    def get_value_by_label(self, label: str) -> str:
        """
        Trả về giá trị văn bản của phần tử dựa trên nhãn được chỉ định.

        Args:
            label (str): Nhãn của phần tử cần lấy giá trị.

        Returns:
            str: Giá trị văn bản của phần tử hoặc None nếu không tìm thấy.
        """
        try:
            element = self.driver.find_element(
                By.XPATH, f"//label[contains(text(), '{label}')]/following-sibling::div"
            )
            return element.text.strip()
        except NoSuchElementException:
            return None

    def get_text_by_label(self, selector: str, attr: str = "text") -> str:
        """
        Trả về văn bản hoặc thuộc tính của phần tử nếu tìm thấy.

        Args:
            selector (str): Bộ chọn CSS của phần tử cần tìm.
            attr (str, optional): Thuộc tính cần lấy (mặc định là 'text').

        Returns:
            str: Văn bản hoặc giá trị thuộc tính của phần tử, hoặc None nếu không tìm thấy.
        """
        try:
            element = self.driver.find_element(By.CSS_SELECTOR, selector)
            return element.get_attribute(attr).strip() if attr != "text" else element.text.strip()
        except NoSuchElementException:
            return None

    def quit(self) -> None:
        """
        Đóng trình duyệt.
        """
        self.driver.quit()

    def extract_info(self) -> Dict[str, Any]:
        """
        Phương thức này sẽ được ghi đè trong các lớp con để trích xuất dữ liệu cụ thể.

        Returns:
            Dict[str, Any]: Dữ liệu trích xuất.
        """
        return {}

    def is_data_available(self) -> bool:
        """
        Kiểm tra xem có thể lấy dữ liệu từ trình duyệt hay không. Nếu không, tự động làm mới trang.

        Returns:
            bool: True nếu dữ liệu có sẵn, False nếu không.
        """
        try:
            element = self.driver.find_element(By.TAG_NAME, "body")
            return bool(element)
        except NoSuchElementException:
            self.driver.refresh()
            time.sleep(WAIT_TIME)
            return False

    def upload_database(self, db: Session, film_data: Dict[str, Any]) -> None:
        """
        Tải dữ liệu đã trích xuất lên cơ sở dữ liệu.

        Args:
            db (Session): Phiên làm việc với cơ sở dữ liệu.
            film_data (Dict[str, Any]): Dữ liệu phim cần lưu.
        """
        if not self.is_data_available():
            self.driver.refresh()
            time.sleep(WAIT_TIME)
        new_film = create_film(db, film_data)
        print(f"Đã thêm phim: {new_film.title}")

    def extract_list_films_url(self) -> List[str]:
        """
        Trích xuất danh sách URL của các bộ phim.

        Returns:
            List[str]: Danh sách URL của các bộ phim.
        """
        return []  # Cần triển khai trong lớp con

    def extract_list_films(self, db: Session) -> List[Dict[str, Any]]:
        """
        Trích xuất danh sách thông tin phim từ danh sách URL.

        Args:
            db (Session): Phiên làm việc với cơ sở dữ liệu.

        Returns:
            List[Dict[str, Any]]: Danh sách thông tin các bộ phim.
        """
        film_links = self.extract_list_films_url()
        film_list = []

        for link_url in film_links:
            try:
                self.load_page(link_url)
                film_info = self.extract_info()
                if film_info:
                    film = Film(**film_info)
                    self.upload_database(db, film)
                    film_list.append(film_info)
            except WebDriverException as e:
                logging.error("Lỗi Selenium khi xử lý phim %s: %s", link_url, e)

        return film_list

