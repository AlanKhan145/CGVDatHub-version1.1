import time
from typing import Any, Dict, List
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from pymongo.collection import Collection
from config import *
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from database import *


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

    def extract_info(self) -> None:
        """
        Phương thức này sẽ được ghi đè trong các lớp con để trích xuất dữ liệu cụ thể.

        Returns:
            None
        """
        return None

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

    def upload_database(self, col: Collection) -> None:
        """
        Tải dữ liệu đã trích xuất lên cơ sở dữ liệu.

        Args:
            col (Collection): Bộ sưu tập MongoDB nơi lưu trữ dữ liệu.
        """
        if not self.is_data_available():
            time.sleep(WAIT_TIME)  # Chờ dữ liệu sẵn sàng

        data = self.extract_info()
        if data:
            save_to_database(col, data)

    def extract_list_film(self) -> List[Dict[str, Any]]:
        """
        Trích xuất danh sách phim từ trang web.

        Args:
            col (Collection): Bộ sưu tập MongoDB nơi lưu trữ dữ liệu.

        Returns:
            List[Dict[str, Any]]: Danh sách các phim trích xuất được.
        """
        return []
