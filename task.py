class Task:
    def __init__(self, id, name, points, frequency, time, start_date, description=None, end_date=None):
        self.id = id
        self.name = name
        self.description = description
        self.points = points
        self.frequency = frequency
        self.time = time
        self.start_date = start_date
        self.end_date = end_date

    def __str__(self):
        return f'{self.id}: {self.name}\n{self.description}\n{self.points} points\n{self.frequency} at {self.time}'

class TaskInstance:
    def __init__(self, id, task_id, name, status, time, description=None):
        self.id = id
        self.task_id = task_id
        self.name = name
        self.description = description
        self.status = status
        self.time = time

    def __str__(self):
        return f'{self.id}: {self.task_id} - {self.status} - {self.date}'