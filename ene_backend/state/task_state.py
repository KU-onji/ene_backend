from datetime import datetime, timedelta

import reflex as rx
from sqlmodel import case, or_, select

from ..db_model import CompleteTask, Task
from .auth import AuthState


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


class TaskTableState(AuthState):
    tasks: list[Task] = []
    comp_tasks: list[CompleteTask] = []
    current_task: Task = Task()
    memo: str = ""
    search_value: str = ""
    sort_value: str = "日付"
    fav: int = 0

    def get_task(self, task: Task):
        self.current_task = task

    def complete_task(self, task: Task):
        with rx.session() as session:
            delete_task = session.exec(select(Task).where(Task.id == task["id"])).first()
            if delete_task is not None:
                session.delete(delete_task)
            else:
                raise RuntimeError("The instance is already deleted from database.")
            session.commit()
        self.load_entries()

        task.pop("id")
        task["complete_date"] = datetime.now()
        with rx.session() as session:
            session.add(CompleteTask(**task))
            session.commit()
        self.comp_load_entries()

    def cancel(self, task: CompleteTask):
        with rx.session() as session:
            delete_task = session.exec(select(CompleteTask).where(CompleteTask.id == task["id"])).first()
            session.delete(delete_task)
            session.commit()
        self.comp_load_entries()

        task.pop("id")
        task.pop("complete_date")
        with rx.session() as session:
            session.add(Task(**task))
            session.commit()
        self.load_entries()

    def calculate_fav(self):
        sum_duration = 0
        for task in self.comp_tasks:
            sum_duration += int(task.hour) * 60 + int(task.minute)
        return min(int((sum_duration / 720) * 100), 100)

    def update_task(self, input_dict: dict):
        if input_alert(input_dict):
            return rx.window_alert("必要な項目が入力されていません")
        if datetime.fromisoformat(input_dict["deadline"]) < datetime.now():
            return rx.window_alert("締切日時は現在時刻より後の日時を指定してください")
        deadline = input_dict["deadline"]
        deadline = deadline.replace("-", "/").replace("T", " ")
        input_dict["deadline_convert"] = deadline
        if not validate_time(input_dict["hour"], input_dict["minute"]):
            return rx.window_alert("所要時間の形式が正しくありません")
        input_dict["user_id"] = self.user_id
        input_dict["color"] = "black"
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
        if datetime.fromisoformat(input_dict["deadline"]) < datetime.now():
            return rx.window_alert("締切日時は現在時刻より後の日時を指定してください")
        deadline = input_dict["deadline"]
        deadline = deadline.replace("-", "/").replace("T", " ")
        input_dict["deadline_convert"] = deadline
        if not validate_time(input_dict["hour"], input_dict["minute"]):
            return rx.window_alert("所要時間の形式が正しくありません")
        input_dict["user_id"] = self.user_id
        input_dict["color"] = "black"
        self.current_task = input_dict
        with rx.session() as session:
            session.add(Task(**self.current_task))
            session.commit()
        self.load_entries()

    def filter_values(self, search_value):
        self.search_value = search_value
        self.load_entries()

    def sort_values(self, sort_value: str):
        self.sort_value = sort_value
        self.load_entries()

    def load_entries(self) -> list[Task]:
        """Get all users from the database."""
        with rx.session() as session:
            session.expire_on_commit = False
            query = select(Task).where(Task.user_id == self.user_id)

            if self.search_value != "":
                search_value = f"%{self.search_value.lower()}%"
                query = query.where(
                    or_(
                        Task.name.ilike(search_value),
                        Task.category.ilike(search_value),
                    )
                )

            if self.sort_value:
                if self.sort_value == "優先度":
                    order = case({"高": 1, "中": 2, "低": 3}, value=Task.priority)
                    query = query.order_by(order).order_by(Task.deadline)
                else:
                    query = query.order_by(Task.deadline)

            self.tasks = session.exec(query).all()

            for task in self.tasks:
                if datetime.now() > datetime.fromisoformat(task.deadline):
                    task.color = "red"
                    session.add(task)  # 変更をマーク
                    session.commit()
                elif datetime.now() + timedelta(days=1) > datetime.fromisoformat(task.deadline):
                    task.color = "orange"
                    session.add(task)
                    session.commit()
        self.comp_load_entries()

    @rx.var
    def str_task_list(self) -> list[str]:
        return [f"{task.name}" for task in self.tasks]

    def comp_load_entries(self) -> list[Task]:
        """Get all users from the database."""
        with rx.session() as session:
            query = select(CompleteTask).where(CompleteTask.user_id == self.user_id)
            query = query.where(CompleteTask.complete_date < datetime.now() - timedelta(days=7))
            delete_tasks = session.exec(query).all()
            if delete_tasks is not None:
                for task in delete_tasks:
                    session.delete(task)
                session.commit()

        with rx.session() as session:
            query = select(CompleteTask).where(CompleteTask.user_id == self.user_id)
            if self.search_value != "":
                search_value = f"%{self.search_value.lower()}%"
                query = query.where(
                    or_(
                        CompleteTask.name.ilike(search_value),
                        CompleteTask.category.ilike(search_value),
                    )
                )

            query = query.order_by(CompleteTask.deadline)

            self.comp_tasks = session.exec(query).all()
            self.fav = self.calculate_fav()
