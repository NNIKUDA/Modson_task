from elasticsearch import Elasticsearch
from os import getenv

ELASTIC_PASSWORD = getenv("ELASTIC_PASSWORD")
ELASTIC_HOST = getenv("ELASTIC_HOST")


# elastic_client = Elasticsearch(
#     f"https://{ELASTIC_HOST}:9200",
#     ca_certs="./http_ca.crt",
#     basic_auth=("elastic", ELASTIC_PASSWORD)
# )
elastic_client = Elasticsearch(
    hosts=f'http://{ELASTIC_HOST}:9200',
    basic_auth=("elastic", "elastic")
)

