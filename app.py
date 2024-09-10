from flask import Flask, render_template, request, redirect, url_for
from datetime import datetime, date

import database

app = Flask(__name__)

# Routes

@app.route('/')
def index():
    today = date.today()

    today_tasks = database.get_task_instances_by_date(today.strftime('%Y-%m-%d'))
    today_tasks = sorted(today_tasks, key=lambda x: x.time)

    all_tasks = database.get_tasks()
    all_tasks = sorted(all_tasks, key=lambda x: x.name)

    return render_template('index.html', all_tasks=all_tasks, 
                           today_tasks=today_tasks, date=today)

@app.route('/add_task', methods=['GET', 'POST'])
def add_task():
    if request.method == 'POST':
        name = request.form['name']
        points = int(request.form['points'])
        frequency = request.form['frequency']
        time = request.form['time']
        start_date = request.form['start_date']
        description = request.form.get('description')
        end_date = request.form.get('end_date')

        database.insert_task(name, points, frequency, time,
                              start_date, description, end_date)
        
        return redirect(url_for('index'))
    
    return render_template('add_task.html')

@app.route('/edit_task/<int:task_id>', methods=['GET', 'POST'])
def edit_task(task_id):
    task = database.get_task(task_id)
    print(task)
    if request.method == 'POST':
        name = request.form['name']
        points = int(request.form['points'])
        frequency = request.form['frequency']
        time = request.form['time']
        start_date = request.form['start_date']
        description = request.form.get('description')
        end_date = request.form.get('end_date')

        database.update_task(task_id, name, points, frequency, time,
                              start_date, description, end_date)

        return redirect(url_for('index'))

    return render_template('edit_task.html', task=task)

@app.route('/update_task_instance_status/<int:instance_id>', methods=['POST'])
def update_task_instance_status(instance_id):
    status = request.form['status']
    database.update_task_instance_status(instance_id, status)
    return redirect(url_for('index'))

@app.route('/remove_task/<int:task_id>')
def remove_task(task_id):
    database.remove_task(task_id)
    return redirect(url_for('index'))


# Filters

@app.template_filter('format_time')
def format_time(value):
    time_obj = datetime.strptime(str(value), '%H:%M:%S')
    return time_obj.strftime('%H:%M')

# Run the app

if __name__ == '__main__':
    app.run(debug=True)
