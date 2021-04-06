from airflow.models import DAG
from airflow.operators.bash import BashOperator
from airflow.operators.subdag import SubDagOperator
from subdags.subdag_parallel_dag import subdag_parallel_dag
from airflow.utils.task_group import TaskGroup

from datetime import datetime

default_args = {
    'start_date' : datetime(2021,1,1)
}

templated_command = """
cd /home/airflow/node
node app.js
sleep 10
"""

with DAG("parallel_dag",schedule_interval='@daily',default_args=default_args,catchup=False) as dag:
    batch1 = BashOperator(
        task_id='bash1',
        bash_command='sleep 3'
    )
    with TaskGroup('processing_tasks') as processing_tasks:
        batch2 = BashOperator(
            task_id='bash2',
            bash_command=templated_command,
            params={'x':'hi'}
        )
        batch3 = BashOperator(
            task_id='bash3',
            bash_command='sleep 3'
        )   
    batch4 = BashOperator(
        task_id='bash4',
        bash_command='sleep 3'
    )

    batch1 << [processing_tasks] << batch4