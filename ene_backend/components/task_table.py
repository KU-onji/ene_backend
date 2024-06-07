import re

import reflex as rx

from ..db_task import Task
from ..state.task_state import TaskTableState


def convert_date(date):
    print(str(date))
    convert = re.findall(r"[0-9]{4}-[0-9]{2}-[0-9]{2}T[0-9]{2}:[0-9]{2}", str(date))
    print(convert)
    if convert:
        return rx.text(convert[0].replace("-", "/").replace("T", " "))
    else:
        return date


def show_task(task: Task):
    """Show a task in a table row."""
    return rx.table.row(
        rx.table.cell(task.name),
        rx.table.cell(task.priority),
        rx.table.cell(task.category),
        rx.table.cell(convert_date(task.deadline)),
        rx.table.cell(
            rx.dialog.root(
                rx.dialog.trigger(
                    rx.button(
                        "詳細",
                        on_click=lambda: TaskTableState.get_task(task),
                    ),
                ),
                rx.dialog.content(
                    rx.form(
                        rx.dialog.title("タスク詳細"),
                        rx.flex(
                            rx.text("名前:"),
                            rx.input(name="name", default_value=task.name, required=True),
                            rx.text("優先度"),
                            rx.select(["低", "中", "高"], default_value=task.priority, name="priority"),
                            rx.text("カテゴリ"),
                            rx.input(name="category", default_value=task.category),
                            rx.text("締切日時:"),
                            rx.input(
                                name="deadline", type="datetime-local", default_value=task.deadline, required=True
                            ),
                            rx.text("詳細:"),
                            rx.text_area(name="memo", default_value=task.memo),
                            direction="column",
                            spacing="3",
                        ),
                        rx.flex(
                            rx.dialog.close(
                                rx.button(
                                    "閉じる",
                                    color_scheme="gray",
                                    variant="soft",
                                ),
                            ),
                            rx.dialog.close(
                                rx.button(
                                    "更新",
                                    color_scheme="green",
                                    variant="soft",
                                    type="submit",
                                ),
                            ),
                            rx.dialog.close(
                                rx.button(
                                    "削除", color_scheme="red", variant="soft", on_click=TaskTableState.delete_task
                                ),
                            ),
                            spacing="3",
                            margin_top="16px",
                            justify="end",
                        ),
                        on_submit=TaskTableState.update_task,
                    ),
                ),
            )
        ),
    )


def task_table() -> rx.Component:
    return rx.vstack(
        rx.input(
            placeholder="Search here...",
            on_change=lambda value: TaskTableState.filter_values(value),
        ),
        rx.scroll_area(
            rx.table.root(
                rx.table.header(
                    rx.table.row(
                        rx.table.column_header_cell("名前"),
                        rx.table.column_header_cell("優先度"),
                        rx.table.column_header_cell("カテゴリ"),
                        rx.table.column_header_cell("締切日時"),
                        rx.table.column_header_cell("詳細"),
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
