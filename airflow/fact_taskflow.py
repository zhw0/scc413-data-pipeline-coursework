import hashlib
from datetime import datetime, timedelta

import pendulum
import requests
from elasticsearch import Elasticsearch
from pymongo.errors import DuplicateKeyError

from airflow.decorators import dag, task
from airflow.hooks.base import BaseHook
from airflow.providers.mongo.hooks.mongo import MongoHook


@dag(
    schedule=timedelta(seconds=10),
    start_date=pendulum.datetime(2023, 1, 1, tz="UTC"),
    catchup=False,
    tags=["fact-data-pipeline"],
)
def fact_taskflow():
    @task
    def get_cat_fact():
        uri = BaseHook.get_connection("cat_api").get_uri()
        response = requests.get(uri)
        cat_fact = response.json()
        return cat_fact

    @task
    def cat_fact_handler(cat_fact):
        data = {
            "source": "cat_api",
            "get_time": datetime.now().strftime("%m/%d/%Y, %H:%M:%S"),
            "fact_info": cat_fact["data"][0],
            "raw_response": cat_fact,
        }
        return data

    @task()
    def get_useless_fact():
        uri = BaseHook.get_connection("useless_fact_api").get_uri()
        print(uri)
        response = requests.get(uri)
        useless_fact = response.json()
        return useless_fact

    @task
    def useless_fact_handler(useless_fact):
        data = {
            "source": "useless_api",
            "get_time": datetime.now().strftime("%m/%d/%Y, %H:%M:%S"),
            "fact_info": useless_fact["text"],
            "raw_response": useless_fact,
        }
        return data

    @task
    def get_black_history_fact():
        uri = BaseHook.get_connection("black_history_api").get_uri()
        response = requests.get(
            "https://rest.blackhistoryapi.io/fact/random?length=4096",
            headers={"x-api-key": "aG9uZ3podmYxVGh1IEFwciAyMCAyMD"},
        )
        black_history_fact = response.json()
        return black_history_fact

    @task
    def black_history_fact_handler(black_history_fact):
        data = {
            "source": "black_history_api",
            "get_time": datetime.now().strftime("%m/%d/%Y, %H:%M:%S"),
            "fact_info": black_history_fact["Results"][0]["text"],
            "raw_response": black_history_fact,
        }
        return data

    @task
    def add_data_to_mongo(data):
        hook = MongoHook(conn_id="mongo_net")
        client = hook.get_conn()
        db = client["scc413"]
        currency_collection = db["fact_data"]
        print(data["fact_info"])
        data["_id"] = hashlib.md5(data["fact_info"].encode()).hexdigest()
        try:
            currency_collection.insert_one(data)
        except DuplicateKeyError:
            print("Duplicate data fetched.")
        else:
            data["fact_hash_id"] = data["_id"]
            del data["_id"]
            return data

    @task
    def add_data_to_es(data):
        uri = BaseHook.get_connection("elasticsearch_loc").get_uri()
        es = Elasticsearch([uri])
        res = es.index(index="test-index", body=data)

    data = get_cat_fact()
    data = cat_fact_handler(data)
    data = add_data_to_mongo(data)
    # add_data_to_es(data)

    data = get_useless_fact()
    data = useless_fact_handler(data)
    data = add_data_to_mongo(data)
    # add_data_to_es(data)

    data = get_black_history_fact()
    data = black_history_fact_handler(data)
    data = add_data_to_mongo(data)
    # add_data_to_es(data)


fact_taskflow()
