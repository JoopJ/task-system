from pushbullet import Pushbullet
from dotenv import load_dotenv
import os

from task import TaskInstance

load_dotenv()
pb = Pushbullet(os.getenv('PUSHBULLET_API_KEY'))

def send_task_notification(task_instance: TaskInstance):
    title = f"{task_instance.name} is due at {task_instance.time.seconds//3600}:{(task_instance.time.seconds//60)%60}"
    body = f"{task_instance.description}"
    pb.push_note(title, body)