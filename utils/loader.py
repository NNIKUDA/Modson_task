import os

from elasticsearch import Elasticsearch, helpers
from psycopg2 import connect
import csv
import codecs
from os import getenv

HOST = getenv("POSTGRES_HOST")
USER = getenv("POSTGRES_USER")
PASSWORD = getenv("POSTGRES_PASSWORD")
DATABASE = getenv("POSTGRES_DB")
SQLALCHEMY_DATABASE_URL = f"postgresql://{USER}:{PASSWORD}@{HOST}:5432/{DATABASE}"

ELASTIC_PASSWORD = getenv("ELASTIC_PASSWORD")
ELASTIC_HOST = getenv("ELASTIC_HOST")

# client = Elasticsearch(
#     f"http://{ELASTIC_HOST}:9200",
#     basic_auth=("elastic", ELASTIC_PASSWORD)
# )
client = Elasticsearch(
    hosts=f'http://{ELASTIC_HOST}:9200',
    basic_auth=("elastic", "elastic")
)

INDEX = "posts"
POSTS_PATH = os.getenv("POSTS_PATH")


def load_data_to_elasrtic_from_csv(filename: str = POSTS_PATH):
    with codecs.open(filename, "r", "utf_8_sig") as csvfile:
        actions = []
        reader = csv.reader(csvfile)
        next(reader)
        id, rows_counter = 1, 0
        for doc_text, _, _ in reader:
            action = {"index": {"_index": INDEX, "_id": id}}
            doc = {
                "id": id,
                "text": doc_text,
            }
            actions.append(action)
            actions.append(doc)
            id += 1
            rows_counter += 1

        client.bulk(index=INDEX, operations=actions)

        # Check the results:
        result = client.count(index=INDEX)
        print(f"elastic: {rows_counter} | {result.body['count']}")


def load_data_to_postgresql_from_csv(filename: str = POSTS_PATH):
    conn = connect(SQLALCHEMY_DATABASE_URL)
    with conn.cursor() as cur:
        cur.execute("DROP TABLE IF EXISTS posts;")
        cur.execute("""CREATE TABLE posts(
               id SERIAL PRIMARY KEY,
               rubrics text[] NOT NULL,
               text text NOT NULL,
               created_date timestamp NOT NULL
           )
           """)
        rows_counter = 0
        with codecs.open(filename, "r", "utf_8_sig") as csvfile:
            reader = csv.reader(csvfile)
            next(reader)
            for doc_text, date, rubrics in reader:
                sql = "INSERT INTO posts (rubrics, text, created_date) VALUES  (%s, %s, %s)"
                cur.execute(sql, (eval(rubrics), doc_text, date))
                rows_counter += 1
            conn.commit()

            cur.execute('SELECT COUNT(*) FROM public.posts')
            print(f"postgresql: {rows_counter} | {cur.fetchall()[0][0]}")


def main():
    load_data_to_elasrtic_from_csv()
    load_data_to_postgresql_from_csv()


if __name__ == "__main__":
    main()
