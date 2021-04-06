from airflow.models import DAG
from datetime import datetime
from airflow.providers.sqlite.operators.sqlite import SqliteOperator
from airflow.providers.http.sensors.http import HttpSensor
from airflow.providers.http.operators.http import SimpleHttpOperator
from airflow.operators.python import PythonOperator
from airflow.operators.bash import BashOperator
from airflow.models import Variable

default_args = {
    'start_date' : datetime(2021,1,1)
}

with DAG('fec_lead_importer',schedule_interval='*/10 * * * *',default_args=default_args,catchup=False) as dag:

    data = Variable.get('importer',deserialize_json=True)

    fec=data["fec"]
    print(fec)

    command = fec["script"] + " --client \'" + fec["client"] + "\' --upsert \'" + fec["upsert"] + "\'"
    run_script = BashOperator(
        task_id='main',
        bash_command = command
    )
