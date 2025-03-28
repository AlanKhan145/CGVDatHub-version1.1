import logging
from typing import Any, Dict, List
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException, WebDriverException
from extractor.base_extractor import Extractor


class CgvExtractor(Extractor):
    """
    Lớp con kế thừa từ Extractor để trích xuất thông tin phim.
    """

    def extract_list_films_url(self) -> List[str]:
        """
        Trích xuất danh sách URL của các bộ phim.

        Returns:
            List[str]: Danh sách URL của các bộ phim.
        """
        try:
            film_links = [
                film.get_attribute("href")
                for film in self.driver.find_elements(By.CSS_SELECTOR, "a.product-image")
            ]
            return film_links
        except WebDriverException as e:
            logging.error(f"Lỗi khi tải trang: {e}")
            return []

    def extract_info(self) -> Dict[str, Any]:
        """
        Trích xuất thông tin chi tiết của một bộ phim từ trang web.

        Returns:
            Dict[str, Any]: Thông tin chi tiết của bộ phim.
        """
        film_info = {}
        try:
            # Lấy tiêu đề phim
            try:
                title_element = self.driver.find_element(
                    By.CSS_SELECTOR, "div.product-name span.h1"
                )
                film_info["title"] = title_element.text.strip()
            except NoSuchElementException:
                film_info["title"] = "Không có thông tin"

            # Lấy các thông tin khác
            film_info["genre"] = self.get_value_by_label("Thể loại")
            film_info["duration"] = self.get_value_by_label("Thời lượng")
            film_info["release_date"] = self.get_value_by_label("Khởi chiếu")
            film_info["director"] = self.get_value_by_label("Đạo diễn")
            film_info["language"] = self.get_value_by_label("Ngôn ngữ")
            film_info["rated"] = self.get_value_by_label("Rated")

            # Lấy thông tin diễn viên
            film_info["actors"] = (
                self.get_value_by_label("Diễn viên")
                or self.get_value_by_label("Diễn viên chính")
                or "Không có thông tin"
            )

            # Lấy mô tả phim
            try:
                description_element = self.driver.find_element(
                    By.CSS_SELECTOR, "meta[name='description']"
                )
                film_info["description"] = description_element.get_attribute("content").strip()
            except NoSuchElementException:
                film_info["description"] = None

            # Lấy các định dạng công nghệ phim
            try:
                technology_elements = self.driver.find_elements(
                    By.CSS_SELECTOR, "div.movie-technology-icons a.movie-detail-icon-type span"
                )
                film_info["technologies"] = [
                    tech.text.strip() for tech in technology_elements if tech.text.strip()
                ]
            except NoSuchElementException:
                film_info["technologies"] = []

            # Lấy poster phim
            try:
                poster_element = self.driver.find_element(
                    By.CSS_SELECTOR, "img#image-main.gallery-image.visible"
                )
                film_info["poster"] = poster_element.get_attribute("src")
            except NoSuchElementException:
                film_info["poster"] = None

            # Kiểm tra vé có sẵn không
            film_info["ticket_available"] = bool(
                self.driver.find_elements(By.CSS_SELECTOR, "button.btn-booking")
            )
        except Exception as e:
            logging.error(f"Lỗi khi lấy thông tin phim: {e}")
            return {}

        return film_info

