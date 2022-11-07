from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.models import Variable
from datetime import datetime


def _process(path, filename):
    print(f'{path} {filename}')

with DAG('Dag_ETL', start_date=datetime(2022, 10, 10), schedule_interval='@daily', catchup=False) as dag:

    task_a = PythonOperator(
        task_id="task_deca",
        python_callable=_process,
        op_kwargs=Variable.get("my_dag_settings", deserialize_json=True)
    )
 

    task_a
    

'''
       op_kwargs={
            "filename": "{{ var.value.teste_excom.py }}"
            
        }
    )


'''

