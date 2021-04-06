from airflow.models import DAG
from datetime import datetime
from airflow.providers.sqlite.operators.sqlite import SqliteOperator
from airflow.providers.http.sensors.http import HttpSensor
from airflow.providers.http.operators.http import SimpleHttpOperator
from airflow.operators.python import PythonOperator
from airflow.operators.bash import BashOperator

import json

from pandas import json_normalize

default_args = {
    'start_date' : datetime(2021,1,1)
}

def _processing_user(ti):
    users=ti.xcom_pull(task_ids=['extract_users'])
    if not(users) or 'results' not in users[0]:
        raise ValueError("No user value exists")
    user = users[0]['results'][0]
    proccessed_user = json_normalize({
        'firstName' : user['name']['first'],
        'lastName' : user['name']['last'],
        'country' : user['location']['country'],
        'username' : user['login']['username'],
        'password' : user['login']['password'],
        'email' : user['email']
    })

    proccessed_user.to_csv('/tmp/users.csv',index=None,header=False)

 

with DAG('data_processing',schedule_interval='@daily',default_args=default_args,catchup=True) as dag:

    creating_table = SqliteOperator(
        task_id='creating_table',
        sqlite_conn_id='db_sqlite',
        sql='''
            Create table if not exists userstwos(
                email text not null primary key,
                password text not null,
                fname text not null
            );
            '''
    )

    is_api_available = HttpSensor(
        task_id='is_api_available',
        http_conn_id='user_api',
        endpoint='api/'
    )

    extracting_users = SimpleHttpOperator(
        task_id='extract_users',
        http_conn_id='user_api',
        endpoint='api/',
        method='GET',
        response_filter=lambda response : json.loads(response.text),
        log_response=True
    )

    processing_user = PythonOperator(
        task_id='processing_user',
        python_callable=_processing_user
    )

    storing_user = BashOperator(
        task_id='storing_user',
        bash_command='echo -e ".separator "," \n. import /tmp/users.csv userstwos" | sqlite3 /home/airflow/airflow/airflow.db'
    )

    creating_table >> is_api_available >> extracting_users >> processing_user >> storing_user