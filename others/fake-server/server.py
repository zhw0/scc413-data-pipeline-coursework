import json
import time
from datetime import datetime

import requests
from pymongo import MongoClient


def get_cat_data():
    client = MongoClient()
    db = client["local_data"]
    collection = db["cat_data"]

    url = "http://127.0.0.1:5000"

    for i in range(10):
        response = requests.get(url=url)
        cat_data = response.json()
        collection.insert_one(cat_data)


def get_uesless_data():
    client = MongoClient("localhost", 27017)
    db = client["local_data"]
    collection = db["useless_data"]

    url = "https://uselessfacts.jsph.pl/api/v2/facts/random"

    for i in range(1000):
        response = requests.get(url=url)
        useless_data = response.json()
        print(useless_data)
        collection.insert_one(useless_data)
        time.sleep(10)
        print(datetime.now())


def get_black_history_data():
    client = MongoClient()
    db = client["local_data"]
    collection = db["black_history_data"]

    for i in range(5):
        url = "https://rest.blackhistoryapi.io/fact/random?length=4096"
        headers = {"x-api-key": "aG9uZ3podmYxVGh1IEFwciAyMCAyMD"}
        response = requests.get(url=url, headers=headers)
        black_history_data = response.json()
        collection.insert_one(black_history_data)
        time.sleep(10)


def extract_data():
    client = MongoClient()
    db = client["local_data"]
    col = db["useless_data"]

    data = []

    for item in col.find():
        del item["_id"]
        data.append(item)

    data = data[:10]

    with open("useless_example.json", "w") as f:
        json.dump(data, f, indent=4)


if __name__ == "__main__":
    extract_data()
