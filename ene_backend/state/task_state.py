import reflex as rx
from sqlmodel import or_, select

from ..db_task import Task


class TaskTableState(rx.State):
    tasks: list[Task] = []
    current_task: Task = Task()
    memo: str = ""

    search_value = ""

    def get_task(self, task: Task):
        self.current_task = task

    def update_task(self, input_dict: dict):
        deadline = input_dict["deadline"]
        deadline = deadline.replace("-", "/").replace("T", " ")
        input_dict["deadline_convert"] = deadline
        self.current_task.update(input_dict)
        with rx.session() as session:
            task = session.exec(select(Task).where(Task.id == self.current_task["id"])).first()
            for field in Task.get_fields():
                if field != "id":
                    setattr(task, field, self.current_task[field])
            session.add(task)
            session.commit()
        self.load_entries()

    def delete_task(self):
        with rx.session() as session:
            task = session.exec(select(Task).where(Task.id == self.current_task["id"])).first()
            session.delete(task)
            session.commit()
        self.load_entries()

    def add_task_to_db(self, input_dict: dict):
        deadline = input_dict["deadline"]
        deadline = deadline.replace("-", "/").replace("T", " ")
        input_dict["deadline_convert"] = deadline
        self.current_task = input_dict
        with rx.session() as session:
            session.add(Task(**self.current_task))
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
