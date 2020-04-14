"""
Code that goes along with the Airflow located at:
http://airflow.readthedocs.org/en/latest/tutorial.html
"""
import airflow
from airflow import DAG
from airflow.operators.bash_operator import BashOperator
from airflow.operators.python_operator import PythonOperator
from datetime import datetime, timedelta
import requests
import json
import os



args = {
    "owner": "airflow",
    "start_date": airflow.utils.dates.days_ago(5),
    "provide_context": True,
    "email": ["airflow@airflow.com"],
    "email_on_failure": False,
    "email_on_retry": False,
    "retries": 2,
    "retry_delay": timedelta(minutes=1),
}

dag = DAG(dag_id='cta_api',
          default_args=args,
          schedule_interval='*/1 * * * *',
          dagrun_timeout=timedelta(seconds=120))

def print_context(ds, **kwargs):
        
    API_KEY = 'XSrApHqi7EJP62TBQFQYe4xms'         #os.environ.get("CTA_KEY")
    print(API_KEY)
    resp = requests.get(f'http://www.ctabustracker.com/bustime/api/v2/getpredictions?key={API_KEY}&stpid=1149&format=json')
    resp_dict = json.loads(resp.text)

    print(resp_dict['bustime-response']['prd'][1])
    print(len(resp_dict['bustime-response']['prd']))
    if resp.status_code != 200:
        raise ApiError('GET /tasks/ {}'.format(resp.status_code))
    for x, ele in enumerate(resp_dict['bustime-response']['prd']):
        call_time = resp_dict['bustime-response']['prd'][x]['tmstmp']
        arr_predict_type = resp_dict['bustime-response']['prd'][x]['typ']
        stop_name = resp_dict['bustime-response']['prd'][x]['stpnm']
        stop_id = resp_dict['bustime-response']['prd'][x]['stpid']
        bus_id = resp_dict['bustime-response']['prd'][x]['vid']
        distance_to_stop = resp_dict['bustime-response']['prd'][x]['dstp']
        route = resp_dict['bustime-response']['prd'][x]['rt']
        direction = resp_dict['bustime-response']['prd'][x]['rtdir']
        end_dest = resp_dict['bustime-response']['prd'][x]['des']
        predicted_arr = resp_dict['bustime-response']['prd'][x]['prdtm']
        tablockid = resp_dict['bustime-response']['prd'][x]['tablockid']
        trip_id = resp_dict['bustime-response']['prd'][x]['tatripid']
        delay = resp_dict['bustime-response']['prd'][x]['dly']
        predicted_ct_dn = resp_dict['bustime-response']['prd'][x]['prdctdn']
        zone = resp_dict['bustime-response']['prd'][x]['zone']
        print('{}, {}, {}, {}, {}'.format(stop_id, route, call_time, predicted_ct_dn, bus_id))
    return 'Whatever you return gets printed in the logs'


run_this = PythonOperator(
    task_id='print_the_context',
    provide_context=True,
    python_callable=print_context,
    dag=dag,
)

run_this