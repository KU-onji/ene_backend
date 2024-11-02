from datetime import datetime

import reflex as rx


class User(rx.Model, table=True):
    address: str
    password: str
    name: str
    google: bool


class Task(rx.Model, table=True):
    user_id: str
    name: str
    priority: str
    category: str
    deadline: str
    deadline_convert: str
    hour: str
    minute: str
    memo: str


class CompleteTask(rx.Model, table=True):
    user_id: str
    name: str
    priority: str
    category: str
    deadline: str
    deadline_convert: str
    hour: str
    minute: str
    memo: str
    complete_date: datetime
