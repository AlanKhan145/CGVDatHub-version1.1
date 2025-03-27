import logging
import time
from typing import Any, Dict, List
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException, WebDriverException
from extractor.base_extractor import Extractor


class MotchillExtractor(Extractor):
    """
    Lớp con kế thừa từ Extractor để trích xuất thông tin phim.
    """

    def get_value_by_label(self, label: str) -> str:
        """
        Tìm và trích xuất giá trị dựa trên nhãn (label) trong danh sách thông tin phim.
        """
        try:
            element = self.driver.find_element(
                By.XPATH, f"//dt[contains(text(), '{label}')]/following-sibling::dd"
            )
            return element.text.strip()
        except NoSuchElementException:
            return "Không có thông tin"

    def extract_list_film(self) -> List[Dict[str, Any]]:
        """
        Trích xuất danh sách phim từ tất cả các trang.

        Returns:
            List[Dict[str, Any]]: Danh sách thông tin các bộ phim.
        """
        film_list = []
        page_links = self.get_all_page_links()

        for page_url in page_links:
            try:
                self.load_page(page_url)
                film_links = [
                    film.find_element(By.CSS_SELECTOR, "a").get_attribute("href")
                    for film in self.driver.find_elements(By.CSS_SELECTOR, "li.item.no-margin-left1")
                ]

                for link_url in film_links:
                    try:
                        self.load_page(link_url)
                        film_info = self.extract_info()
                        if film_info:
                            film_info["link"] = link_url
                            film_list.append(film_info)
                    except WebDriverException as e:
                        logging.error("Lỗi Selenium khi xử lý phim %s: %s", link_url, e)

            except WebDriverException as e:
                logging.error("Lỗi khi tải trang %s: %s", page_url, e)

        return film_list

    def extract_info(self) -> Dict[str, Any]:
        """
        Trích xuất thông tin chi tiết của một bộ phim từ trang web.
        """
        film_info = {}
        try:
            try:
                title_element = self.driver.find_element(By.TAG_NAME, "title")
                film_info["title"] = title_element.get_attribute("textContent").split(" - ")[0].strip()
            except NoSuchElementException:
                film_info["title"] = "Không có thông tin"

            film_info["status"] = self.get_value_by_label("Trạng thái")
            film_info["director"] = self.get_value_by_label("Đạo diễn")
            film_info["duration"] = self.get_value_by_label("Thời lượng")
            film_info["episodes"] = self.get_value_by_label("Số tập")
            film_info["language"] = self.get_value_by_label("Ngôn ngữ")
            film_info["release_year"] = self.get_value_by_label("Năm sản xuất")
            film_info["country"] = self.get_value_by_label("Quốc gia")

            film_info["genre"] = ", ".join([
                genre.text.strip()
                for genre in self.driver.find_elements(By.XPATH, "//dt[contains(text(), 'Thể loại')]/following-sibling::dd/a")
            ]) or "Không có thông tin"

            film_info["actors"] = ", ".join([
                actor.text.strip()
                for actor in self.driver.find_elements(By.XPATH, "//dt[contains(text(), 'Diễn viên')]/following-sibling::dd/a")
            ]) or "Không có thông tin"

            try:
                description_element = self.driver.find_element(By.CSS_SELECTOR, "meta[name='description']")
                film_info["description"] = description_element.get_attribute("content").strip()
            except NoSuchElementException:
                film_info["description"] = "Không có thông tin"

            try:
                poster_element = self.driver.find_element(By.CSS_SELECTOR, "div.poster img")
                film_info["poster"] = poster_element.get_attribute("src")
            except NoSuchElementException:
                film_info["poster"] = "Không có thông tin"

        except Exception as e:
            logging.error("Lỗi khi lấy thông tin phim: %s", e)
            return {}

        return film_info

    def get_all_page_links(self) -> List[str]:
        """
        Lấy danh sách tất cả các trang có phim.

        Returns:
            List[str]: Danh sách link các trang.
        """
        page_links = []

        while True:
            try:
                current_url = self.driver.current_url
                if current_url not in page_links:
                    page_links.append(current_url)

                try:
                    next_button = self.driver.find_element(By.CSS_SELECTOR, "a.next.page-numbers")
                    next_button.click()
                    time.sleep(2)
                except NoSuchElementException:
                    logging.info("Không còn trang tiếp theo.")
                    break

            except WebDriverException as e:
                logging.error("Lỗi khi lấy danh sách trang: %s", e)
                break

        return page_links

