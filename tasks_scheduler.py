#!/usr/bin/env python3

import schedule
import psycopg2 as psy
import random
import time
import datetime
from dotenv import load_dotenv, find_dotenv
import os


# Parse a .env file and then load all the variables found as environment variables.
load_dotenv(find_dotenv())


def job():
    # Railway postgreSQL
    connect = psy.connect(
        host = os.getenv('HOST'),
        port = os.getenv('PORT'),
        user = os.getenv('USER'),
        password = os.getenv('PASSWORD'),
        dbname = os.getenv('DBNAME')
    )

    cur = connect.cursor()

    # Get all Menus and store data in a dict
    query = f'select * from inventory_menu;'
    cur.execute(query)
    rows = cur.fetchall()

    menus = list()

    for row in rows:
        id = row[0]
        name = row[1]
        price = row[3]
        type = row[6]
        available = row[5]
        menus.append({
            'id': id,
            'name': name,
            'price': price,
            'type': type,
            'available': available
        })

    # Order count
    COUNTER = random.randint(0, 5)

    for _ in range(COUNTER):
        # Get a random available finger foods
        fingers = [m for m in menus if m['type'] == "Finger Foods" and m['available']]
        # print(fingers)
        choice = random.choice(fingers)
        print(choice)
        query = f"insert into inventory_purchase (menu_id, price, purchase_date) values({choice['id']}, {choice['price']}, current_timestamp);"
        cur.execute(query)
        connect.commit()
        time.sleep(1)

        # Get a random available starters
        starters = [m for m in menus if m['type'] == "Entrée" and m['available']]
        # print(starters)
        choice = random.choice(starters)
        print(choice)
        query = f"insert into inventory_purchase (menu_id, price, purchase_date) values({choice['id']}, {choice['price']}, current_timestamp);"
        cur.execute(query)
        connect.commit()
        time.sleep(1)

        # Get a random available plat
        plats = [m for m in menus if m['type'] == "Plat" and m['available']]
        # print(plats)
        choice = random.choice(plats)
        print(choice)
        query = f"insert into inventory_purchase (menu_id, price, purchase_date) values({choice['id']}, {choice['price']}, current_timestamp);"
        cur.execute(query)
        connect.commit()
        time.sleep(1)

        # Get a random available dessert
        desserts = [m for m in menus if m['type'] == "Dessert" and m['available']]
        # print(desserts)
        choice = random.choice(desserts)
        print(choice)
        query = f"insert into inventory_purchase (menu_id, price, purchase_date) values({choice['id']}, {choice['price']}, current_timestamp);"
        cur.execute(query)
        connect.commit()
        time.sleep(1)

    print("Purchase Done")

    connect.close()

lunch = '12:30:00'
dinner = '19:30:00'
fmt = '%H:%M:%S'

schedule.every().monday.at('12:30').do(job)
schedule.every().monday.at('19:30').do(job)

schedule.every().tuesday.at('12:30').do(job)
schedule.every().tuesday.at('19:30').do(job)

schedule.every().wednesday.at('12:30').do(job)
schedule.every().wednesday.at('19:30').do(job)

schedule.every().thursday.at('12:30').do(job)
schedule.every().thursday.at('19:30').do(job)

schedule.every().friday.at('12:30').do(job)
schedule.every().friday.at('19:30').do(job)

schedule.every().saturday.at('12:30').do(job)
schedule.every().saturday.at('19:30').do(job)


while True:
    schedule.run_pending()

    t = datetime.datetime.now()
    print(f'Running task scheduler: {datetime.datetime.now()}')

    if int(t.hour) >= int(lunch[:2]) and int(t.hour) <= int(dinner[:2]):
        tdelta = datetime.datetime.strptime(dinner, FMT) - datetime.datetime.strptime(f'{t.hour}:{t.minute}:00', fmt)
        print(f'Next service is dinner in {tdelta}')

    if int(t.hour) <= int(lunch[:2]) or int(t.hour) >= int(dinner[:2]):
        tdelta = datetime.datetime.strptime(lunch, fmt) - datetime.datetime.strptime(f'{t.hour}:{t.minute}:00', fmt)
        print(f'Next service is lunch in {tdelta}')

    time.sleep(3600)
