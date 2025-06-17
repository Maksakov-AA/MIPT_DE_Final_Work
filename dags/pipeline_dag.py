from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime
import sys

# ✅ Указываем полный путь к каталогу с etl-модулями
sys.path.append("/root/ml_pipeline_project/etl")

from load_data import load_and_split
from preprocessing import preprocess
from train_model import train_model
from evaluate import evaluate

default_args = {
    "owner": "admin",
    "start_date": datetime(2024, 1, 1),
    "retries": 1
}

with DAG(
    dag_id="ml_pipeline_dag",
    default_args=default_args,
    schedule_interval='@daily',
    catchup=False,
    tags=["ml", "etl"]
) as dag:

    task_load_data = PythonOperator(
        task_id="load_data",
        python_callable=load_and_split
    )

    task_preprocess_train = PythonOperator(
        task_id="preprocess_train",
        python_callable=lambda: preprocess("data/train.csv", "data/processed/train.csv")
    )

    task_preprocess_test = PythonOperator(
        task_id="preprocess_test",
        python_callable=lambda: preprocess("data/test.csv", "data/processed/test.csv")
    )

    task_train = PythonOperator(
        task_id="train_model",
        python_callable=lambda: train_model("data/processed/train.csv", "models/model.pkl")
    )

    task_evaluate = PythonOperator(
        task_id="evaluate_model",
        python_callable=lambda: evaluate("models/model.pkl", "data/processed/test.csv", "results/metrics.json")
    )

    # Задаём зависимости
    task_load_data >> [task_preprocess_train, task_preprocess_test] >> task_train >> task_evaluate
