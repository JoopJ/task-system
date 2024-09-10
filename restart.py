# Restart the database and insert some test data

import sys
import database
from datetime import datetime

if __name__ == '__main__':

    database.drop_tables()

    database.create_tables()

    today = datetime.today().strftime('%Y-%m-%d')

    database.insert_task(
        name='Make bed', 
        points=1,
        frequency='daily',
        time='09:00',
        start_date=today,
        description='Make bed look presentable',
        end_date='2024-12-31'
    )

    database.insert_task(
        name='Read Book',
        points=2,
        frequency='weekly',
        time='20:00',
        start_date=today,
        description='Read a book for at least 30 minutes'
    )

    database.insert_task(
        name='Water Plant',
        points=0,
        frequency='monthly',
        time='19:00',
        start_date=today,
        description='Water the plant in the living room'
    )

    database.insert_task(
        name='Exercise',
        points=10,
        frequency='yearly',
        time='06:00',
        start_date=today,
        description='Perform your yearly push-up',
        end_date='2024-12-31'
    )

    sys.exit()