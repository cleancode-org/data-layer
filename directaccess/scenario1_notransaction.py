import logging
import psycopg2
from psycopg2.extras import LoggingConnection
from queries import *


def setup_data ():
    conn = psycopg2.connect(**db_settings)
    tim=conn.cursor()
    tim.execute("delete from account;")
    tim.execute("INSERT INTO account(name,balance) VALUES('Bob',10000);")
    tim.execute("INSERT INTO account(name,balance) VALUES('Peter',5000);")
    tim.execute("INSERT INTO account(name,balance) VALUES('Tina',1000);")
    tim.execute("INSERT INTO account(name,balance) VALUES('Peter',500);")
    conn.commit()
    conn.close()
    tim.close()

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

setup_data()
#Lost Update
#the story, Bob is buying a gadget using the shop_app, the gadget costs 1000 dollars and he must have at least 5000 dollar in his account to buy it
# at the same time, the loan agency is processing Bob's application and they plan to approve the loan if he has balance more than or equal 10000
#Bob starts with balance of 10000, after executing the following queries, what should be the final balance of Bob?

def shop ():
    time.sleep(random.random())
    conn = psycopg2.connect(**db_settings)
    conn.autocommit=True
    shop_app = conn.cursor() #user shop - session 1   
    shop_app.execute("select balance from account where name = 'Bob';")
    t_balance =shop_app.fetchone()[0]
    print("\nShop app sees balance of Bob as "+str(t_balance))
    time.sleep(random.random())
    if t_balance >5000:
        t_balance -= 1000
        shop_app.execute("update account set balance=(%s) where name='Bob'", (t_balance,))
        print("\nShop app updates Bob's balance to "+str(t_balance))
    #conn.commit()
    #shop_app.close()
    #conn.close()

def loan ():
    time.sleep(random.random())
    conn2 = psycopg2.connect(**db_settings)
    conn2.autocommit=True
    loan_app = conn2.cursor() #user loan - session 2
    loan_app.execute("select balance from account where name = 'Bob';")
    s_balance =loan_app.fetchone()[0]
    print("\nLoan app sees balance of Bob as "+str(s_balance))
    time.sleep(random.random())
    if s_balance >=10000:
        s_balance +=5000
        loan_app.execute("update account set balance=(%s) where name='Bob'", (s_balance,))
        print("\nLoan app updates Bob's balance to "+str(s_balance))

    #conn2.commit()
    #loan_app.close()
    #conn2.close()


import threading


import time
import random
import threading


threads = [
    threading.Thread(target=shop, name="shop_app"),
    threading.Thread(target=loan, name="loan_app"),
]

for t in threads:
    t.start()




