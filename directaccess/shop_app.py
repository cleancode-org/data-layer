import logging
import psycopg2
from psycopg2.extras import LoggingConnection
from queries import *


def setup_data (tim):
    tim.execute("delete from accounts;")
    tim.execute("INSERT INTO accounts(name,balance) VALUES('Bob',10000);")
    tim.execute("INSERT INTO accounts(name,balance) VALUES('Peter',5000);")
    tim.execute("INSERT INTO accounts(name,balance) VALUES('Tina',1000);")
    tim.execute("INSERT INTO accounts(name,balance) VALUES('Peter',500);")
    conn.commit()

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

conn2 = psycopg2.connect(connection_factory=LoggingConnection, **db_settings)
conn2.initialize(logger)

shop_app = conn.cursor() #user shop - session 1
loan_app = conn2.cursor() #user loan - session 2

setup_data(shop_app)

#the story, Bob is buying a gadget using the shop_app, the gadget costs 1000 dollars.
# at the same time, the loan agency is processing Bob's application and they plan to approve the loan if he has balance more than or equal 10000
#Bob starts with balance of 10000, after executing the following queries, what should be the final balance of Bob?

shop_app.execute("select balance from accounts where name = 'Bob';")
t_balance =shop_app.fetchone()[0]
print("Tim sees balance of Bob as "+str(t_balance))


if t_balance >5000:
    t_balance -= 1000
    shop_app.execute("update accounts set balance=(%s) where name='Bob'", (t_balance,))

loan_app.execute("select balance from accounts where name = 'Bob';")
s_balance =loan_app.fetchone()[0]
print("Soe sees balance of Bob as "+str(s_balance))

if s_balance >=10000:
    s_balance +=5000
    loan_app.execute("update accounts set balance=(%s) where name='Bob'", (s_balance,))

conn.commit()

conn2.commit()

loan_app.close()
shop_app.close()
conn.close()
conn2.close()





