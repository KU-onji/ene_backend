import reflex as rx


class Task(rx.Model, table=True):
    name: str
    priority: str
    category: str
    deadline: str
    memo: str