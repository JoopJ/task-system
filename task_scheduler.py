from datetime import datetime, date, timedelta
import time
import schedule
import threading
import os

from database import get_task_instances_by_date
from mobile_interaction import send_task_notification

# Flag to ensure only one scheduler is running
scheduler_started = False

def check_tasks():
    # Check all task instances, send notifications if due or due in 5 minutes
    task_instances = get_task_instances_by_date(
        date.today().strftime('%Y-%m-%d'))
    now = datetime.now()
    current_timedelta = timedelta(hours=now.hour, 
        minutes=now.minute, seconds=now.second)
    
    print("Checking tasks at", current_timedelta)

    for task_instance in task_instances:
        print(task_instance.name)
        print(current_timedelta, task_instance.time - timedelta(minutes=5), task_instance.time)
        if (current_timedelta == task_instance.time - timedelta(minutes=5) 
            or current_timedelta == task_instance.time
            and task_instance.status == 'pending'):
            print("Sending notification for:", task_instance)
            send_task_notification(task_instance)


schedule.every().minutes.at(":00").do(check_tasks)

def run_scheduler():
    print("Starting task checker thread...")
    while True:
        schedule.run_pending()
        time.sleep(1)

def start_scheduler():
    global scheduler_started
    # Ensure only one scheduler is running, 
    # even if the app is reloaded in debug mode
    if (not scheduler_started 
        and not os.environ.get('WERKZEUG_RUN_MAIN') == 'true'):
        scheduler_started = True
        scheduler_thread = threading.Thread(target=run_scheduler)
        scheduler_thread.daemon = True
        scheduler_thread.start()
    else:
        print("Scheduler already started")
