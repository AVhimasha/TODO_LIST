from flask import Blueprint, render_template, redirect, url_for, request
from flask_login import login_required, current_user
from model import db, Task
from datetime import datetime, timedelta

task = Blueprint('task', __name__)

@task.route('/')
@login_required
def index():
    tasks = Task.query.filter_by(user_id=current_user.id).all()

    # History for the last 5 days
    today = datetime.today().date()
    history = []
    for i in range(5):
        day = today - timedelta(days=i)
        completed_tasks = Task.query.filter_by(
            user_id=current_user.id,
            completed=True,
            due_date=day
        ).all()
        history.append({
            'date': day,
            'tasks': [task.content for task in completed_tasks]
        })
    history.reverse()  # So the oldest day is first

    return render_template('index.html', tasks=tasks, history=history)

@task.route('/add', methods=['POST'])
@login_required
def add():
    content = request.form.get('content')
    due_date_str = request.form.get('due_date')
    due_date = datetime.strptime(due_date_str, '%Y-%m-%d').date() if due_date_str else None
    if content:
        task = Task(content=content, user_id=current_user.id, due_date=due_date)  # type: ignore
        db.session.add(task)
        db.session.commit()
    return redirect(url_for('task.index'))

@task.route('/complete/<int:task_id>')
@login_required
def complete(task_id):
    task = Task.query.get_or_404(task_id)
    if task.user_id == current_user.id:
        task.completed = not task.completed
        db.session.commit()
    return redirect(url_for('task.index'))

@task.route('/delete/<int:task_id>')
@login_required
def delete(task_id):
    task = Task.query.get_or_404(task_id)
    if task.user_id == current_user.id:
        db.session.delete(task)
        db.session.commit()
    return redirect(url_for('task.index'))

@task.route('/close/<int:task_id>')
@login_required
def close(task_id):
    task = Task.query.get_or_404(task_id)
    if task.user_id == current_user.id:
        task.completed = True
        db.session.commit()
    return redirect(url_for('task.index'))
