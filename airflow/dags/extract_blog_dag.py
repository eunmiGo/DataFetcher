from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime, timedelta

from extract_blog.extract_blog_url import ExtractBlogUrl
from extract_keyword import extract_keyword
from load.load_data import LoadData
from load.load_meta_data import LoadMetaData

default_args = {
    'owner': 'admin',
    'start_date': datetime(2023, 9, 19),
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

dag = DAG(
    dag_id='extract_blog_dag',
    default_args=default_args,
    description='Extract Data From blog and Load To DB DAG',
    schedule_interval=None,
)


def crawling_blog_def(**kwargs):
    extractor = ExtractBlogUrl('검색어 입력')
    try:
        path_list = extractor.blog_crawler()
        kwargs['ti'].xcom_push(key='path_list', value=path_list)
    except Exception as e:
        print("fetch data blog def error")
        raise Exception(e)


def extract_keyword_def(**kwargs):
    ti = kwargs['ti']
    path_list = ti.xcom_pull(task_ids='crawling_portal_task', key='path_list')
    if path_list is not None:
        extract_keyword.extract_keyword(path_list)
    else:
        print("No data received")


def load_blog_def(**kwargs):
    ti = kwargs['ti']
    data = ti.xcom_pull(task_ids='crawling_blog_task', key='path_list')
    bucket_name = ti.xcom_pull(task_ids='crawling_blog_task', key='bucket_name')
    loader = LoadData(data, bucket_name)
    if data:
        minio_path_list, file_size, bucket_name = loader.load_data()
        kwargs['ti'].xcom_push(key='minio_path_list', value=minio_path_list)
        kwargs['ti'].xcom_push(key='file_size', value=file_size)
        kwargs['ti'].xcom_push(key='bucket_name', value=bucket_name)
    else:
        print("No data received")


def load_blog_meta_def(**kwargs):
    ti = kwargs['ti']
    minio_path_list = ti.xcom_pull(task_ids='load_blog_task', key='minio_path_list')
    file_size = ti.xcom_pull(task_ids='load_blog_task', key='file_size')
    loader = LoadMetaData(minio_path_list, file_size)
    if minio_path_list:
        loader.load_meta_data()


crawling_blog_task = PythonOperator(
    task_id='crawling_blog_task',
    python_callable=crawling_blog_def,
    dag=dag,
    do_xcom_push=True
)
extract_keyword_task = PythonOperator(
    task_id='extract_blog_task',
    python_callable=extract_keyword_def,
    dag=dag,
    do_xcom_push=True
)
load_blog_task = PythonOperator(
    task_id='load_blog_task',
    python_callable=load_blog_def,
    dag=dag,
)

load_blog_meta_task = PythonOperator(
    task_id='load_blog_meta_task',
    python_callable=load_blog_meta_def,
    dag=dag,
)

crawling_blog_task >> extract_keyword_task >> load_blog_task >> load_blog_meta_task
