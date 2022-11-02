from airflow.operators.python import PythonOperator
from airflow.providers.postgres.operators.postgres import PostgresOperator, PostgresHook
from airflow.utils.task_group import TaskGroup
from typing import Any
from datetime import datetime, timedelta
import json

from airflow.decorators import dag, task

postgres_conn_id='postgres_default'
@dag(
    start_date=datetime(2022, 10, 10),
    max_active_runs=3,
    schedule_interval=None,
    catchup=False,
  
)
def get_postgre_databases() -> Any:
    pg_hook = PostgresHook(postgres_conn_id=postgres_conn_id)
    @task
    def select_marcas():
        conn = pg_hook.get_conn()
        cursor = conn.cursor()
        cursor.execute("select *from CadastroProduto.Marcas")
        dags = cursor.fetchall()
        return json.dumps(dags)

    select_marcas()


    
reporting_dag = get_postgre_databases()