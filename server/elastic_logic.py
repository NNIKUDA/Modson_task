import elasticsearch

from elastic import Elasticsearch


def search_posts_by_text(client: Elasticsearch, text: str, index_name: str, limit: int = 20):
    try:
        search_result = client.search(index=index_name, body={"size": 20, "query": {"match": {"text": text}}})
        return [hit["_source"]["id"] for hit in search_result["hits"]["hits"]]
    except elasticsearch.NotFoundError as _:
        return []


def delete_post_by_id(client: Elasticsearch, index_name: str, post_id: int = 1):
    return client.delete(index=index_name, id=post_id)
