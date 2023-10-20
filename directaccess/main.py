import logging
import psycopg2
from psycopg2.extras import LoggingConnection
from queries import *


logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

from config import (
    DATABASE_HOST,
    DATABASE_USERNAME,
    DATABASE_PASSWORD,
    DATABASE_PORT,
    DATABASE_NAME,
)

db_settings = {
    "user":  DATABASE_USERNAME,
    "password": DATABASE_PASSWORD,
    "host": DATABASE_HOST,
    "database": DATABASE_NAME,
}
conn = psycopg2.connect(connection_factory=LoggingConnection, **db_settings)
conn.initialize(logger)

cur = conn.cursor()

#select_all_one(cur)
#select_all_two(cur)
#select_all_three(cur)


#insert(cur)


#select_count_rows(cur)

cur.close()






