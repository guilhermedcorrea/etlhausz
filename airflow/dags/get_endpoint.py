from airflow.decorators import dag, task
from airflow.utils.dates import days_ago
from typing import Dict
import requests
import logging
import os
from dotenv import load_dotenv

load_dotenv()

API_KEY_EMISSAO = os.getenv('API_KEY')
COMPANY_ID_EMISSAO = os.getenv('COMPANY_ID')
endpoint = os.getenv('ENDPOINT')

API = endpoint


default_args = {
    'start_date': days_ago(1),
}

@dag(schedule_interval='@daily', default_args=default_args, catchup=True)
def get_all_nfe_supply():

    @task
    def get_endpoint_all_notas() -> Dict[str, float]:
        return requests.get(API).json()

    @task()
    def obtem_jsons(response: Dict[str, float]) -> Dict[str, float]:
        logging.info(response)
        return {'productInvoices': response['productInvoices']}

    @task
    def armazena_valores(data: Dict[str, float]):
        logging.info(f"issuer: {data['issuer']} transport {data['productInvoices']}")

    armazena_valores(obtem_jsons(get_endpoint_all_notas()))

dag = get_all_nfe_supply()