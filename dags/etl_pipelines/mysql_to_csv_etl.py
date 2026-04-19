"""
ETL Pipeline: MySQL to CSV
Extracts data from MySQL, transforms, and loads to CSV
"""

from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime, timedelta
import pandas as pd
import pymysql
import os
from dotenv import load_dotenv

load_dotenv()

# Configuration from environment
MYSQL_CONFIG = {
    'host': os.getenv('MYSQL_HOST', 'localhost'),
    'user': os.getenv('MYSQL_USER', 'root'),
    'password': os.getenv('MYSQL_PASSWORD', 'root'),
    'database': os.getenv('MYSQL_DATABASE', 'etl_example')
}

OUTPUT_DIR = os.path.join(os.path.dirname(__file__), '../../data/output')

def extract_from_mysql(**context):
    """Extract data from MySQL"""
    print(f"Extracting from MySQL: {MYSQL_CONFIG['database']}")
    
    connection = pymysql.connect(**MYSQL_CONFIG)
    query = "SELECT * FROM sample_data"
    df = pd.read_sql(query, connection)
    connection.close()
    
    print(f"Extracted {len(df)} records")
    context['ti'].xcom_push(key='extracted_data', value=df.to_json())
    return len(df)

def transform_data(**context):
    """Transform data - filter age > 30"""
    data_json = context['ti'].xcom_pull(key='extracted_data', task_ids='extract')
    df = pd.read_json(data_json)
    
    print(f"Original records: {len(df)}")
    df_transformed = df[df['age'] > 30].copy()
    print(f"Transformed records (age > 30): {len(df_transformed)}")
    
    context['ti'].xcom_push(key='transformed_data', value=df_transformed.to_json())
    return len(df_transformed)

def load_to_csv(**context):
    """Load transformed data to CSV"""
    data_json = context['ti'].xcom_pull(key='transformed_data', task_ids='transform')
    df = pd.read_json(data_json)
    
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    file_path = os.path.join(OUTPUT_DIR, f'etl_output_{timestamp}.csv')
    
    df.to_csv(file_path, index=False)
    print(f"Data loaded to {file_path}")
    
    return file_path

default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': datetime(2024, 1, 1),
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=1),
}

dag = DAG(
    'mysql_to_csv_etl',
    default_args=default_args,
    description='ETL pipeline from MySQL to CSV',
    schedule_interval='@daily',
    catchup=False,
    tags=['etl', 'mysql', 'csv'],
)

extract = PythonOperator(task_id='extract', python_callable=extract_from_mysql, dag=dag)
transform = PythonOperator(task_id='transform', python_callable=transform_data, dag=dag)
load = PythonOperator(task_id='load', python_callable=load_to_csv, dag=dag)

extract >> transform >> load
