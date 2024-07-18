import pathlib
import re

import pandas as pd

from task_2.config import logger
from task_2.database import connect_db
from task_2.src.parse_files import SeleniumParse


class ExportingDataToDB:
    """
    Класс для получения данных из .xls файлов, их анализа и обработки, загрузки в БД
    """

    dir = pathlib.Path.cwd() / "excel_files"

    def __init__(self):
        self.start_parse = SeleniumParse().get_page_number()

    def get_data_for_files(self) -> pd.DataFrame:
        """
        Метод для для получения данных из .xls файлов, подготовке данных для экспорта в БД
        """
        global df
        for file in self.dir.iterdir():
            if file.is_file():
                df = pd.read_excel(io=file, engine="xlrd", index_col=None)
                date_filter = re.sub(r"\D", "", file.name)[:8]
                correct_date = (
                    date_filter[:4] + "." + date_filter[4:6] + "." + date_filter[6:8]
                )

                index = (
                        df[df["Форма СЭТ-БТ"] == "Единица измерения: Метрическая тонна"].index[0]
                        + 1
                )
                df = df.iloc[index:, [1, 2, 3, 4, 5, 14]]
                df.rename(
                    columns={
                        "Форма СЭТ-БТ": "exchange_product_id",
                        "Unnamed: 2": "exchange_product_name",
                        "Unnamed: 3": "delivery_basis_name",
                        "Unnamed: 4": "volume",
                        "Unnamed: 5": "total",
                        "Unnamed: 14": "count",
                    },
                    inplace=True,
                )
                df = df[df["count"] != "-"]
                df.insert(loc=2, column="oil_id", value=df["exchange_product_id"].str[:4])
                df.insert(
                    loc=3,
                    column="delivery_basis_id",
                    value=df["exchange_product_id"].str[4:7],
                )
                df.insert(
                    loc=5,
                    column="delivery_type_id",
                    value=df["exchange_product_id"].str[-1],
                )
                df.insert(loc=9, column="date", value=correct_date)
                df = df.fillna("-")
                df = df.iloc[2:]
                df = df.iloc[:-2]

            yield df

    def export_data_to_db(self) -> None:
        """
        Метод для загрузки данных в БД
        """
        dataframe = self.get_data_for_files()
        connection = connect_db()
        try:
            for df_item in dataframe:
                df_item.to_sql(
                    "spimex_trading_results",
                    connection,
                    if_exists="append",
                    index=False,
                )
            logger.info("Данные загружены в БД")
        except Exception as ex:
            logger.exception("Ошибка добавления данных в БД: " + str(ex), exc_info=True)
