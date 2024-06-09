import reflex as rx
from sqlmodel import or_, select

from ..db_task import Task


def validate_time(hour: str, minute: str) -> bool:
    if not hour.isdecimal() or not minute.isdecimal():
        return False

    if not 0 <= int(minute) <= 59:
        return False

    return True


def input_alert(input_dict: dict) -> bool:
    if input_dict["name"] == "":
        return True
    if input_dict["priority"] == "":
        return True
    if input_dict["deadline"] == "":
        return True
    if input_dict["hour"] == "":
        return True
    if input_dict["minute"] == "":
        return True

    return False


class TaskTableState(rx.State):
    tasks: list[Task] = []
    current_task: Task = Task()
    memo: str = ""

    search_value = ""

    def get_task(self, task: Task):
        self.current_task = task

    def update_task(self, input_dict: dict):
        if input_alert(input_dict):
            return rx.window_alert("必要な項目が入力されていません")
        deadline = input_dict["deadline"]
        deadline = deadline.replace("-", "/").replace("T", " ")
        input_dict["deadline_convert"] = deadline
        if not validate_time(input_dict["hour"], input_dict["minute"]):
            return rx.window_alert("所要時間の形式が正しくありません")
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
        if input_alert(input_dict):
            return rx.window_alert("必要な項目が入力されていません")
        deadline = input_dict["deadline"]
        deadline = deadline.replace("-", "/").replace("T", " ")
        input_dict["deadline_convert"] = deadline
        if not validate_time(input_dict["hour"], input_dict["minute"]):
            return rx.window_alert("所要時間の形式が正しくありません")
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

    @rx.var
    def str_task_list(self) -> list[str]:
        return [f"{task.name}" for task in self.tasks]
