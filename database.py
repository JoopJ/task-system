from dotenv import load_dotenv
import os
import mysql.connector
from datetime import datetime, timedelta; from dateutil.relativedelta import relativedelta
from task import Task, TaskInstance

def connect():
    # Connect to MySQL database and return connection and cursor
    load_dotenv()
    conn = mysql.connector.connect(
        host = os.getenv("DB_HOST"),
        user = os.getenv("DB_USER"),
        password = os.getenv("DB_PASSWORD"),
        database = os.getenv("DB_NAME")
    )

    return conn, conn.cursor()

def create_tables():
    # Create tasks and task_instances tables if they don't already exist
    conn, cursor = connect()

    # tasks
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS tasks (
        id INT AUTO_INCREMENT PRIMARY KEY,
        name VARCHAR(255) NOT NULL,
        description VARCHAR(1000),
        points INT NOT NULL,
        frequency ENUM('singular', 'daily', 'weekly', 'monthly', 'yearly') NOT NULL,
        time TIME NOT NULL,
        start_date DATE NOT NULL,
        end_date DATE
    )
    ''')
    # task_instances
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS task_instances (
        id INT AUTO_INCREMENT PRIMARY KEY,
        task_id INT NOT NULL,
        date DATE NOT NULL,
        status ENUM('pending', 'complete',' failed') NOT NULL DEFAULT 'pending',
        points_awarded INT,
        FOREIGN KEY (task_id) REFERENCES tasks(id) ON DELETE CASCADE
    )
    ''')

    conn.commit()
    conn.close()

def insert_task(name, points, frequency, time, start_date, description=None, end_date=None):
    conn, cursor = connect()

    sql = '''
    INSERT INTO tasks (name, description, points, frequency, time, start_date, end_date)
    VALUES (%s, %s, %s, %s, %s, %s, %s)
    '''
    data = (name, 
            description if description else None, 
            points, 
            frequency, 
            time, 
            start_date, 
            end_date if end_date else None)

    cursor.execute(sql ,data)
    conn.commit()
    task_id = cursor.lastrowid

    conn.close()
    insert_task_instances_for_task(task_id, frequency, start_date, end_date)
    return task_id

def insert_task_instance(task_id, date):
    conn, cursor = connect()

    cursor.execute('''
        INSERT INTO task_instances (task_id, date) 
        VALUES (%s, %s)''',
        (task_id, date)
    )
    conn.commit()
    conn.close()    

def insert_task_instances_for_task(task_id, frequency, start_date, end_date):
    conn, cursor = connect()

    # default end date is 31st December of the current year
    if end_date is None or end_date == '':
        end_date = datetime(datetime.now().year, 12, 31).strftime('%Y-%m-%d')

    match frequency:
        case 'singular':
            insert_task_instance(task_id, start_date)

        case 'daily':
            cursor.execute('''
                SELECT DATEDIFF(%s, %s)
                ''', (end_date, start_date))
            days = cursor.fetchone()[0]

            for i in range(days + 1):
                date = datetime.strptime(start_date, '%Y-%m-%d') + timedelta(days=i)
                insert_task_instance(task_id, date.strftime('%Y-%m-%d'))

        case 'weekly':
            cursor.execute('''
                SELECT DATEDIFF(%s, %s)
                ''', (end_date, start_date))
            weeks = cursor.fetchone()[0] // 7

            for i in range(weeks + 1):
                date = datetime.strptime(start_date, '%Y-%m-%d') + timedelta(weeks=i)
                insert_task_instance(task_id, date.strftime('%Y-%m-%d'))
        
        case 'monthly':
            cursor.execute('''
                SELECT TIMESTAMPDIFF(MONTH, %s, %s)
                ''', (start_date, end_date))
            months = cursor.fetchone()[0]

            for i in range(months + 1):
                date = datetime.strptime(start_date, '%Y-%m-%d') + relativedelta(months=i)
                insert_task_instance(task_id, date.strftime('%Y-%m-%d'))

        case 'yearly':
            cursor.execute('''
                SELECT TIMESTAMPDIFF(YEAR, %s, %s)
                ''', (start_date, end_date))
            years = cursor.fetchone()[0]

            for i in range(years + 1):
                date = datetime.strptime(start_date, '%Y-%m-%d') + relativedelta(years=i)
                insert_task_instance(task_id, date.strftime('%Y-%m-%d'))

def get_task(task_id):
    conn, cursor = connect()
    cursor.execute("SELECT * FROM tasks WHERE id = %s", (task_id,))
    result = cursor.fetchone()
    
    if result:
        return Task(id=result[0], name=result[1], description=result[2], 
                    points=result[3], frequency=result[4], time=result[5], 
                    start_date=result[6], end_date=result[7])
    return None


def get_tasks():
    conn, cursor = connect()
    cursor.execute("SELECT * FROM tasks")
    results = cursor.fetchall()
    conn.close()

    return [Task(id=result[0], name=result[1], description=result[2], 
                    points=result[3], frequency=result[4], time=result[5], 
                    start_date=result[6], end_date=result[7]) 
                    for result in results]

# Poorly formatted return, should be a list of TaskInstance objects. TODO: Fix
def get_task_instances():
    conn, cursor = connect()
    cursor.execute("SELECT * FROM task_instances")
    results = cursor.fetchall()
    conn.close()

    return results

def drop_tables():
    # delete all tables
    conn, cursor = connect()
    
    cursor.execute("SHOW TABLES")
    tables = cursor.fetchall()

    for table in tables:
        table_name = table[0]
        cursor.execute(f'DROP TABLE {table_name}')
        print(f'table {table_name} dropped.')

    conn.commit()
    conn.close()

def get_task_instances_by_date(date):
    conn, cursor = connect()
    cursor.execute('''
        SELECT ti.id, ti.task_id, t.name, ti.status, t.time, t.description
        FROM task_instances ti
        JOIN tasks t ON ti.task_id = t.id
        WHERE ti.date = %s
        ''', (date,))
    results = cursor.fetchall()
    conn.close()

    return [TaskInstance(id=result[0], task_id=result[1], name=result[2], 
                         status=result[3], time=result[4], description=result[5]) 
                         for result in results]

def remove_task(task_id):
    conn, cursor = connect()
    cursor.execute("DELETE FROM tasks WHERE id = %s", (task_id,))
    conn.commit()
    conn.close()