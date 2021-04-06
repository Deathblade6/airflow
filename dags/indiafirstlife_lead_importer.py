from airflow.models import DAG
from datetime import datetime
from airflow.operators.bash import BashOperator

default_args = {
    'start_date' : datetime(2021,1,1)
}

with DAG('indiafirstlife_lead_importer',schedule_interval='*/15 * * * *',default_args=default_args,catchup=False) as dag:

    command = "$HOME/workspace/cron-jobs/scripts/standard/leads_importer/import_leads.sh --client \"indiafirstlife\""
    
    run_script = BashOperator(
        task_id='main',
        bash_command = command
    )
