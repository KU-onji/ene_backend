import re

import reflex as rx
from sqlmodel import or_, select

from ..db_task import Task


class TaskTableState(rx.State):
    tasks: list[Task] = []
    input_dict: dict = {}

    sort_value = ""
    search_value = ""

    def add_task_to_db(self, input_dict: dict):
        self.input_dict = input_dict
        name, priority, category, deadline, memo = input_dict.values()
        deadline = re.findall(r"[0-9]{4}-[0-9]{2}-[0-9]{2}T[0-9]{2}:[0-9]{2}", deadline)[0]
        deadline = deadline.replace("-", "/").replace("T", " ")
        with rx.session() as session:
            session.add(Task(name=name, priority=priority, category=category, deadline=deadline, memo=memo))
            session.commit()
        self.load_entries()

    def filter_values(self, search_value):
        self.search_value = search_value
        self.load_entries()

    def load_entries(self) -> list[Task]:
        """Get all users from the database."""
        with rx.session() as session:
            query = select(Task)

            if self.search_value != "":
                search_value = f"%{self.search_value.lower()}%"
                query = query.where(
                    or_(
                        Task.name.ilike(search_value),
                        Task.category.ilike(search_value),
                    )
                )

            query = query.order_by(Task.deadline)

            self.tasks = session.exec(query).all()
