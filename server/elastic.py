from elasticsearch import Elasticsearch


ELASTIC_PASSWORD = "q7vs5kxha_jt_Z2e3HIs"

elastic_client = Elasticsearch(
    "https://localhost:9200",
    ca_certs="./http_ca.crt",
    basic_auth=("elastic", ELASTIC_PASSWORD)
)
