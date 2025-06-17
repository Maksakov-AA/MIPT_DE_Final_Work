# MIPT_DE_Final_Work
Экзаменационная работа МФТИ по предмету Инжиниринг данных

## Тема
Автоматизация и оркестрация пайплайна машинного обучения с использованием Apache Airflow и облачного хранилища.

## Описание задания
Вы инженер данных в медицинском центре, где разрабатываются предиктивные модели диагностики заболеваний. Ваша задача — спроектировать и реализовать автоматизированный ETL-процесс: от получения медицинских данных до выгрузки результатов модели в облачное хранилище с помощью Apache Airflow и Python. 

Результат работы: воспроизводимый проект в виде репозитория с пояснениями в формате README.


# Проект: Автоматизация ML-пайплайна с использованием Apache Airflow

## Цель проекта
Разработать воспроизводимый и надёжный ML-процесс с полной оркестрацией с помощью Apache Airflow, а также обеспечить автоматическое выполнение задач по обучению модели, её оценке и выгрузке результатов в облачное хранилище Google Drive.

## Архитектура проекта
### Проект реализован в виде пайплайна, включающего 5 основных шагов:
### Загрузка и разбиение данных
- Скрипт load_data.py загружает исходный датасет (wdbc_data.csv), делит его на обучающую и тестовую выборки, и сохраняет в data/train.csv и data/test.csv. Это исходная точка всего процесса
### Предобработка данных
- Скрипт preprocessing.py применяет стандартизацию признаков, обработку пропущенных значений (если есть) и кодирование категориальных переменных. Обработанные данные сохраняются в data/processed/
### Обучение модели
- Скрипт train_model.py обучает модель классификации (например, логистическую регрессию или RandomForest) на предварительно обработанных данных. Результирующая модель сохраняется в models/model.pkl
### Оценка модели
- Скрипт evaluate.py применяет обученную модель к тестовой выборке, рассчитывает метрики качества (accuracy, precision, recall, f1-score) и сохраняет их в results/metrics.json
### Выгрузка метрик и модели на Google Drive
- Скрипт upload_to_drive.py авторизуется через сервисный аккаунт (используя credentials.json) и загружает файл с метриками (metrics.json) и/или модель на указанный Google Drive

Все шаги представлены в отдельных модулях Python и объединены в DAG Airflow с названием ml_pipeline_dag.

## Схема пайплайна
![alt text](https://github.com/Maksakov-AA/MIPT_DE_Final_Work/blob/main/images/pipeline_scheme.png?raw=true)

## Структура проекта с описанием скриптов
### ml_pipeline_project/
Корневая директория
- README.md - описание

### ml_pipeline_project/dags/
Директория для DAG файлов
- pipeline_dag.py - DAG-файл для Apache Airflow

### ml_pipeline_project/etl/
Директория для шагов обработки и моделирования
- load_data.py - загружает исходные данные из CSV-файлов. Делит на тренировочную и тестовую выборки, копирует их в папку
- preprocessing.py - выполняет очистку, кодирование категориальных признаков и масштабирование числовых. Обрабатывает данные для последующего обучения модели
- train_model.py - обучает модель (например, RandomForest или другую) на обработанных тренировочных данных и сохраняет результат в models/model.pkl
- evaluate.py - выполняет прогноз на тестовых данных и рассчитывает метрики (accuracy, f1-score и др.). Сохраняет результат в results/metrics.json

### ml_pipeline_project/scripts/
Директория для скриптов
- upload_to_drive.py - Скрипт, который загружает финальные результаты (metrics.json) на Google Drive с использованием сервисного аккаунта и credentials.json

### ml_pipeline_project/data/
Директория для хранения оригинальных датасетов
- train.csv - тренировочная выборка
- test.csv - тестовая выборка

### ml_pipeline_project/data/processed/
Директория для хранения обработанных датасетов (после preprocessing.py)
- train.csv - обработанная тренировочная выборка
- test.csv - обработанная тестовая выборка

### ml_pipeline_project/models/
Директория для хранения моделей
- model.pkl - модель, обученная в train_model.py, готовая к использованию или деплою

### ml_pipeline_project/results/
Итоговые файлы
- metrics.json - файл с метриками качества модели, сформированный в evaluate.py. Используется для отчётности или мониторинга

### ml_pipeline_project/credentials/
Креды
- credentials.json - ключ сервисного аккаунта Google. Используется в upload_to_drive.py для авторизации при загрузке файлов на Google Drive

### ml_pipeline_project/logs/
Папка для логов, создаётся автоматически Airflow. Используется для хранения логов исполнения задач DAG

### ml_pipeline_project/venv/
Виртуальное окружение Python с установленными зависимостями (pandas, scikit-learn, google-api-python-client и т. д.). Используется для изоляции среды.

## Оркестрация пайплайна с помощью Airflow
### Название DAG: ml_pipeline_dag
- Это имя задаётся при создании DAG-объекта в файле pipeline_dag.py
  
### В DAG реализована следующая последовательность шагов, где каждая задача зависит от успешного выполнения предыдущей
- load_data_task: загружает и разбивает датасет.
- preprocess_data_task: зависит от load_data_task, так как обрабатывает только что сохранённые файлы.
- train_model_task: зависит от предобработки, использует обработанный train.csv.
- evaluate_model_task: применяет модель к test.csv и считает метрики.
- upload_to_drive_task: завершающий шаг, отправляющий метрики и/или модель в Google Drive

### Зависимости задаются через метод >>
load_data_task >> preprocess_data_task >> train_model_task >> evaluate_model_task >> upload_to_drive_task

## Инструкция по запуску
### 1. Установка  зависимости:
Переход в директорию проекта и активация виртуального окружения
```bash
cd ~/ml_pipeline_project
source venv/bin/activate
```

Установка зависимостей
```bash
pip install -r requirements.txt
```

### 2. Настройка Airflow
Установка переменной окружения AIRFLOW_HOME:
```bash
export AIRFLOW_HOME=~/ml_pipeline_project/airflow
```

Инициализация базы данных Airflow:
```bash
airflow db init
```

### 3. Создание пользователя Airflow
Создание администратора:
```bash
airflow users create \
  --username admin \
  --firstname Admin \
  --lastname User \
  --role Admin \
  --email admin@example.com \
  --password admin
```

### 4. Запуск Airflow
Запуск web-сервера и планировщика (в отдельных терминалах или в tmux):
```bash
airflow webserver --port 8080
```

```bash
airflow scheduler
```

### 5. Размещение DAG
Файл pipeline_dag.py должен лежать по пути:
```bash
~/ml_pipeline_project/dags/pipeline_dag.py
```

Необходимо убедиться, что переменная AIRFLOW_HOME указывает на:
```bash
~/ml_pipeline_project/airflow
```

### 6. Проверка DAG
Показать структуру DAG:
```bash
airflow dags show ml_pipeline_dag
```

Проверка импорта:
```bash
airflow dags list
```

### 7. Ручной запуск DAG
Тест выполнения отдельной задачи (без запуска всего DAG):
```bash
airflow tasks test ml_pipeline_dag load_data 2025-06-17
```
Запуск всего DAG:
 ```bash
airflow dags trigger ml_pipeline_dag
```

### 8. Просмотр логов задачи
 ```bash
airflow tasks logs ml_pipeline_dag <task_id> <run_id>
```

### 9. Результаты
- Модель сохраняется в: models/model.pkl
- Метрики модели: results/metrics.json
- Загружаются в Google Drive (папка определяется в upload_to_drive.py)

## Интеграция с Google Drive
Файл upload_to_drive.py использует credentials/credentials.json, полученный через Google Cloud Console (OAuth сервисный аккаунт).
- Загружаются два файла: модель и метрики
- Указан folder_id целевой папки

## Надёжность и устойчивость
- Каждый модуль обособлен и логирует ключевые действия
- Airflow retries=2, retry_delay=timedelta(minutes=1) предусмотрены
- При ошибке в одном шаге — DAG останавливается, но шаги изолированы логически

### Потенциальные точки сбоя
- API Google может быть недоступен → предусмотрен retry
- Невалидные данные → предусмотрены проверки на NaN, сохранение промежуточных файлов
- Ошибки модели → try-except блок в train_model.py

### Предложения по развитию
- Добавить Telegram-уведомления о статусе DAG
- Добавить профилирование модели и логирование метрик в MLflow
- Реализовать CI/CD (например, через GitHub Actions)

## Скриншоты работы DAG
![alt text](https://github.com/Maksakov-AA/MIPT_DE_Final_Work/blob/main/images/AirFlow_DAG.png?raw=true)
![alt text](https://github.com/Maksakov-AA/MIPT_DE_Final_Work/blob/main/images/AirFlow_DAG_2.png?raw=true)

## Ссылки
- http://194.87.252.54:8080/dags/ml_pipeline_dag/grid - Ссылка на AirFlow
- https://drive.google.com/drive/folders/1X6MaMZe-YRXfSBLTQuOUia9QkulA4iem - Папка с model.pkl на Google Drive
