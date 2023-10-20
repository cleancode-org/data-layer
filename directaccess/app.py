from log import LOGGER
import logging
from loguru import logger
import psycopg2
import psycopg2.extras

from config import (
    DATABASE_HOST,
    DATABASE_USERNAME,
    DATABASE_PASSWORD,
    DATABASE_PORT,
    DATABASE_NAME,
)



class Database:

    def __init__(
            self,
            DATABASE_HOST,
            DATABASE_USERNAME,
            DATABASE_PASSWORD,
            DATABASE_PORT,
            DATABASE_NAME
        ):
        self.host = DATABASE_HOST
        self.username = DATABASE_USERNAME
        self.password = DATABASE_PASSWORD
        self.port = DATABASE_PORT
        self.dbname = DATABASE_NAME
        self.conn = None

    def connect(self):
        if self.conn is None:
            try:
                self.conn = psycopg2.connect(
                    host=self.host,
                    user=self.username,
                    password=self.password,
                    port=self.port,
                    dbname=self.dbname
                )
            except psycopg2.DatabaseError as e:
                LOGGER.error(e)
                raise e
            finally:
                LOGGER.info('Connection opened successfully.')

    def select_rows(self, query):
        self.connect()
        with self.conn.cursor() as cur:
            cur.execute(query)
            records = cur.fetchall()
        cur.close()
        return records

    def select_rows_dict_cursor(self, query):
        self.connect()
        with self.conn.cursor(cursor_factory = psycopg2.extras.RealDictCursor) as cur:
            cur.execute(query)
            records = cur.fetchall()
        cur.close()
        return records

    def update_rows(self, query):
        self.connect()
        with self.conn.cursor() as cur:
            cur.execute(query)
            self.conn.commit()
            cur.close()
            return f"{cur.rowcount} rows affected."

# Create database class
db = Database(
    DATABASE_HOST,
    DATABASE_USERNAME,
    DATABASE_PASSWORD,
    DATABASE_PORT,
    DATABASE_NAME
)

def display_query_results(rows, cursor_type=None):
    LOGGER.info(f'Results from {cursor_type}:')
    for row in rows:
        LOGGER.info(row)


standard_results = db.select_rows("SELECT * FROM movies inner join movies_actors on movies.movies_id=movies_actors.movies_id inner join actors on actors.actors_id = movies_actors.actors_id;")
display_query_results(standard_results, cursor_type='standard')

dictionary_results = db.select_rows_dict_cursor("SELECT * FROM movies inner join movies_actors on movies.movies_id=movies_actors.movies_id inner join actors on actors.actors_id = movies_actors.actors_id;")
display_query_results(dictionary_results, cursor_type='dictionary')