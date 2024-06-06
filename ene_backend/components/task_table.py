import datetime

import reflex as rx
from sqlmodel import or_, select

from ..db_task import Task


class TaskTableState(rx.State):
    tasks: list[Task] = []

    sort_value = ""
    search_value = ""

    def add_task(self, name, priority, category, deadline):
        deadline = datetime.datetime.strptime(deadline, "%Y-%m-%d")
        with rx.session() as session:
            session.add(Task(name=name, priority=priority, category=category, deadline=deadline))
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


def show_task(task: Task):
    """Show a task in a table row."""
    return rx.table.row(
        rx.table.cell(task.name),
        rx.table.cell(task.priority),
        rx.table.cell(task.category),
        rx.table.cell(task.deadline),
        rx.table.cell(rx.button("詳細")),
    )


def task_table():
    return rx.vstack(
        rx.input(
            placeholder="Search here...",
            on_change=lambda value: TaskTableState.filter_values(value),
        ),
        rx.scroll_area(
            rx.table.root(
                rx.table.header(
                    rx.table.row(
                        rx.table.column_header_cell("Name"),
                        rx.table.column_header_cell("Priority"),
                        rx.table.column_header_cell("Category"),
                        rx.table.column_header_cell("Deadline"),
                        rx.table.column_header_cell("Detail"),
                    ),
                ),
                rx.table.body(
                    rx.foreach(TaskTableState.tasks, show_task),
                ),
                on_mount=TaskTableState.load_entries,
            ),
            type="auto",
            scrollbars="vertical",
            height="15em",
        ),
    )
