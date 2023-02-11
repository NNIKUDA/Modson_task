from elasticsearch import Elasticsearch
from sqlalchemy import create_engine, text
from psycopg2 import connect
import csv
import codecs


def load_data_to_elasrtic_from_csv(filename: str = "posts_example.csv"):
    ELASTIC_PASSWORD = "EJAXt6QKW2wB_Zcwn18r"

    client = Elasticsearch(
        "https://localhost:9200",
        ca_certs="./../http_ca.crt",
        basic_auth=("elastic", ELASTIC_PASSWORD)
    )

    with codecs.open(filename, "r", "utf_8_sig") as csvfile:
        reader = csv.reader(csvfile)
        next(reader)
        id, result = 1, [0, 0]
        for doc_text, _, _ in reader:
            resp = client.index(index="docs", id=id, document={"text": doc_text})
            result[0] += 1
            if resp['result'] in ('cteared', 'updated'):
                result[1] += 1
            id += 1
        print(result[0], result[1])


def load_data_to_postgresql_from_csv(filename: str = "posts_example.csv"):
    conn = connect("postgresql://postgres:postgres@localhost:5432/postgres")
    cur = conn.cursor()

    cur.execute("DROP TABLE IF EXISTS posts;")
    cur.execute("""CREATE TABLE posts(
           id SERIAL PRIMARY KEY,
           rubrics text[] NOT NULL,
           text text NOT NULL,
           created_date timestamp NOT NULL
       )
       """)
    with codecs.open(filename, "r", "utf_8_sig") as csvfile:
        reader = csv.reader(csvfile)
        next(reader)
        for doc_text, date, rubrics in reader:
            sql = "INSERT INTO posts (rubrics, text, created_date) VALUES  (%s, %s, %s)"
            cur.execute(sql, (eval(rubrics), doc_text, date))

        conn.commit()
        print("Успешно записал данные в postgres")


def main():
    load_data_to_elasrtic_from_csv()
    load_data_to_postgresql_from_csv()


if __name__ == "__main__":
    main()
