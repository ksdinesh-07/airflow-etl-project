from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime, timedelta
import pandas as pd
import pymysql
import os
from io import StringIO

MYSQL_CONFIG = {
    'host': 'localhost',
    'user': 'root',
    'password': 'root',
    'database': 'etl_example'
}

OUTPUT_DIR = '/home/dinesh/Documents/ETL_Airflow/data/output'

def extract_from_mysql(**context):
    connection = pymysql.connect(**MYSQL_CONFIG)
    query = 'SELECT * FROM sample_data'
    df = pd.read_sql(query, connection)
    connection.close()
    
    print(f"✅ Extracted {len(df)} records from MySQL")
    # Convert DataFrame to JSON string
    context['ti'].xcom_push(key='extracted_data', value=df.to_json())
    return len(df)

def transform_data(**context):
    data_json = context['ti'].xcom_pull(key='extracted_data', task_ids='extract')
    # Parse JSON string using StringIO
    df = pd.read_json(StringIO(data_json))
    
    print(f"📊 Original records: {len(df)}")
    df_transformed = df[df['age'] > 30].copy()
    print(f"🔄 Transformed records (age > 30): {len(df_transformed)}")
    
    context['ti'].xcom_push(key='transformed_data', value=df_transformed.to_json())
    return len(df_transformed)

def load_to_csv(**context):
    data_json = context['ti'].xcom_pull(key='transformed_data', task_ids='transform')
    df = pd.read_json(StringIO(data_json))
    
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    file_path = os.path.join(OUTPUT_DIR, f'etl_output_{timestamp}.csv')
    
    df.to_csv(file_path, index=False)
    print(f"💾 Data saved to: {file_path}")
    
    return file_path

default_args = {
    'owner': 'dinesh',
    'depends_on_past': False,
    'start_date': datetime(2024, 1, 1),
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=1),
}

dag = DAG(
    'mysql_etl_dag',
    default_args=default_args,
    description='ETL: Extract from MySQL, Transform, Load to CSV',
    schedule_interval=timedelta(minutes=5),
    catchup=False,
    tags=['etl', 'mysql'],
)

extract = PythonOperator(task_id='extract', python_callable=extract_from_mysql, dag=dag)
transform = PythonOperator(task_id='transform', python_callable=transform_data, dag=dag)
load = PythonOperator(task_id='load', python_callable=load_to_csv, dag=dag)

extract >> transform >> load
