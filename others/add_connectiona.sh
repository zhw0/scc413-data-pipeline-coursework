airflow connections add 'cat_api' \
    --conn-uri 'http://127.0.0.1:5000'

airflow connections add 'useless_fact_api' \
    --conn-uri 'https://uselessfacts.jsph.pl/api/v2/facts/random'

airflow connections add 'black_history_api' \
    --conn-uri 'https://rest.blackhistoryapi.io/fact/random?length=4096'

airflow connections add 'mongo_net' \
    --conn-uri 'mongodb://127.0.0.1:27017'

airflow connections add 'elasticsearch_loc' \
    --conn-uri 'http://127.0.0.1:9200'