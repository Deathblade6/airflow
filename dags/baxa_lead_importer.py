from airflow.models import DAG
from datetime import datetime,timedelta
from airflow.operators.bash import BashOperator

default_args = {
    'start_date' : datetime(2021,1,1)
}

with DAG('baxa_lead_importer',schedule_interval='*/10 * * * *',default_args=default_args,catchup=False) as dag:

    command = "sleep 20"
    
    run_script = BashOperator(
        task_id='main',
        retries=1,
        retry_delay=timedelta(seconds=5),
        email = ['arun.padmanabhan00@gmail.com'],
        email_on_failure = True,
        execution_timeout=timedelta(seconds=30),
        bash_command = command
    )