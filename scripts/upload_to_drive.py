import os
import logging
from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload

# Настройка логирования
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def upload_file_to_drive():
    try:
        # Абсолютный путь к credentials.json
        creds_path = os.path.join(os.path.dirname(__file__), '..', 'credentials', 'credentials.json')
        creds_path = os.path.abspath(creds_path)

        # Аутентификация через service account
        creds = service_account.Credentials.from_service_account_file(
            creds_path,
            scopes=['https://www.googleapis.com/auth/drive.file']
        )

        # Инициализация клиента Google Drive
        service = build('drive', 'v3', credentials=creds)

        # Путь к файлу модели
        file_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'models', 'model.pkl'))

        # ID папки на Google Drive
        folder_id = '1X6MaMZe-YRXfSBLTQuOUia9QkulA4iem'

        file_metadata = {
            'name': 'model.pkl',
            'parents': [folder_id]
        }

        media = MediaFileUpload(file_path, mimetype='application/octet-stream')

        file = service.files().create(
            body=file_metadata,
            media_body=media,
            fields='id'
        ).execute()

        logger.info(f"Файл успешно загружен на Google Drive. ID: {file.get('id')}")

    except Exception as e:
        logger.error(f"Ошибка при загрузке файла: {e}")

if __name__ == '__main__':
    upload_file_to_drive()