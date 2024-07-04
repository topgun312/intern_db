import pathlib
import time
from datetime import datetime

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager

from task_2.config import SITE_URL, logger


chrome_options = Options()
chrome_options.add_argument("--headless")
chrome_options.add_argument("--disable-gpu")
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-extensions")
chrome_options.add_argument("--incognito")
chrome_options.add_argument("--disable-infobars")
chrome_options.add_argument("--log-level=3")
chrome_options.add_experimental_option(
    "prefs",
    {
        "download.default_directory": "/home/topgun/PycharmProjects/intern_db/task_2/excel_files",
        "download.prompt_for_download": False,
        "download.directory_upgrade": True,
        "safebrowsing.enabled": True,
    },
)

service = Service(ChromeDriverManager().install())


class SeleniumParse:
    """
    Класс для скачивания .xls - файлов с сайта spimex.com и сохранения их в директорию excel_files
    """

    def __init__(self):
        self.driver = webdriver.Chrome(service=service, options=chrome_options)
        self.create_dir = self.create_exfiles_dir()

    def download_files_on_page(self, PAGE_URL: str) -> None:
        """
        Метод для скачивания файлов с одной страницы сайта с 01.01.2023 года по настоящее время
        """
        self.driver.get(PAGE_URL)
        files = self.driver.find_elements(By.CLASS_NAME, "accordeon-inner__wrap-item")
        for file in files[:10]:
            format_date = file.find_element(By.TAG_NAME, "span").get_attribute(
                "textContent"
            )
            current_date = datetime.strptime(format_date, "%d.%m.%Y").date()
            end_date = datetime.strptime("01.07.2024", "%d.%m.%Y").date()
            if current_date < end_date:
                return
            else:
                link_locator = file.find_element(By.TAG_NAME, "a")
                self.driver.execute_script("arguments[0].click();", link_locator)
                time.sleep(2)

    def get_page_number(self) -> None:
        """
        Метод для перебора всех страниц и вызова метода download_files_on_page для каждой страницы
        :return:
        """
        logger.info("Начинаю загрузку файлов с сайта!")
        try:
            for page in range(1, 367):
                result = self.download_files_on_page(SITE_URL + f"?page=page-{page}")
                if not result:
                    logger.info("Загрузка файлов в папку excel_files завершена!")
                    break
                logger.info(f"Страница {page} обработана полностью!")
                time.sleep(2)
        except Exception as ex:
            logger.exception("Ошибка загрузки файлов: " + str(ex), exc_info=True)

    def create_exfiles_dir(self) -> None:
        """
        Метод для создания(инициализации) папки excel_files
        :return:
        """
        dir = pathlib.Path.cwd() / "excel_files"
        if not dir.exists() and not dir.is_dir():
            dir.mkdir(exist_ok=True)
            logger.info("Директория excel_files создана!")
        else:
            logger.info("Директория excel_files инициализирована!")
