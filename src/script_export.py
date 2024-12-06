import csv
import json
import os

from sqlalchemy import create_engine, MetaData, Table
import pandas as pd


DATABASE_URI = 'postgresql://postgres:123@localhost:5432/postgres'
engine = create_engine(DATABASE_URI)


data_directory = 'data'
if not os.path.exists(data_directory):
    os.makedirs(data_directory)

# Функция для экспорта всех таблиц в указанный формат
def export_all_tables(engine, export_format='csv'):
    meta = MetaData()
    meta.reflect(bind=engine)  # Загружает схемы всех таблиц

    # Перебираем все таблицы в базе данных
    for table_name in meta.tables:
        table = meta.tables[table_name]

        # Получаем данные из таблицы
        with engine.connect() as connection:
            query = table.select()
            result = connection.execute(query).fetchall()

            # Получаем имена столбцов
            columns = [column.name for column in table.columns]

            # Форматируем данные
            data = [dict(zip(columns, row)) for row in result]

            # Сохраняем данные в указанный формат
            if export_format == 'csv':
                file_name = os.path.join(data_directory, f"{table_name}.csv")
                with open(file_name, mode='w', newline='', encoding='utf-8') as file:
                    writer = csv.writer(file)
                    writer.writerow(columns)  # Запись заголовков
                    writer.writerows(result)  # Запись данных
                print(f"Экспортировано в CSV: {file_name}")

            elif export_format == 'json':
                file_name = os.path.join(data_directory, f"{table_name}.json")
                with open(file_name, mode='w', encoding='utf-8') as file:
                    json.dump(data, file, ensure_ascii=False, indent=4)  # Запись данных в JSON
                print(f"Экспортировано в JSON: {file_name}")

            else:
                print("Неподдерживаемый формат экспорта")

# Запуск функции экспорта с указанием формата (например, 'csv' или 'json')
export_format = input("Введите формат экспорта (csv или json): ").strip().lower()
export_all_tables(engine, export_format)