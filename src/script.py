import os
import subprocess
import requests

# Настройки
DB_NAME = f'postgres'
DB_USER = f'postgres'
DB_PASSWORD = '123'
BACKUP_FILE = f"postgres_backup_schedule.sql"
YANDEX_DISK_TOKEN = 'y0_AgAAAABjE9PrAAzndwAAAAEbJihBAABc9WQJ085Lz4p2Fzad4OisO1iRuw'
YADISK_FOLDER_PATH = f'backups/'  # путь на Яндекс Диск


# Создание бэкапа базы данных
def create_backup():
    os.environ['PGPASSWORD'] = DB_PASSWORD
    try:
        subprocess.run(['pg_dump', '-U', DB_USER, DB_NAME, '-f', f'C:\\Users\\1levt\\PycharmProjects\\PythonProject\\tgBot\\src\\{BACKUP_FILE}'], check=True)
        print(f"Backup of database '{DB_NAME}' created successfully as '{BACKUP_FILE}'")
    except subprocess.CalledProcessError as e:
        print(f"Error occurred while creating backup: {e}")


# Получение URL для загрузки на Яндекс Диск
def get_upload_url():
    headers = {
        'Authorization': f'OAuth {YANDEX_DISK_TOKEN}'
    }
    response = requests.get(
        f'https://cloud-api.yandex.net/v1/disk/resources/upload?path={YADISK_FOLDER_PATH}{BACKUP_FILE}&overwrite=true',
        headers=headers
    )

    if response.status_code == 200:
        return response.json().get('href')
    else:
        print(f"Error occurred while getting upload URL: {response.text}")
        return None


# Загрузка файла на Яндекс Диск
def upload_to_yandex_disk(upload_url):
    with open(f'C:\\Users\\1levt\\PycharmProjects\\PythonProject\\tgBot\\src\\{BACKUP_FILE}', 'rb') as file:
        response = requests.put(upload_url, data=file)

    if response.status_code == 201:
        print(f"Backup '{BACKUP_FILE}' uploaded to Yandex Disk at '{YADISK_FOLDER_PATH}'")
    else:
        print(f"Error occurred while uploading to Yandex Disk: {response.text}")


if __name__ == '__main__':
    create_backup()
    upload_url = get_upload_url()
    if upload_url:
        upload_to_yandex_disk(upload_url)
