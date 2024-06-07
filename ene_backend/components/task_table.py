import reflex as rx

from ..db_task import Task
from ..state.task_state import TaskTableState


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
