import time

from task_2.config import logger
from task_2.database import create_db
from task_2.src.export_info_to_db import ExportingDataToDB


def main():
    """
    Основная функция для вызова работы всего скрипта
    :return:
    """
    create_db()
    exp_data = ExportingDataToDB()
    exp_data.export_data_to_db()


if __name__ == "__main__":
    start_time = time.time()
    main()
    finish_time = time.time()
    work_time = round(finish_time - start_time, 1)
    logger.info(f"Операция выполнена успешно. Время работы: {work_time} секунд")
