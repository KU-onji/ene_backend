import reflex as rx

from ..db_model import CompleteTask
from ..state.task_state import TaskTableState


def show_task(task: CompleteTask):
    """Show a task in a table row."""
    return rx.table.row(
        rx.table.cell(task.name),
        rx.table.cell(task.priority),
        rx.table.cell(task.category),
        rx.table.cell(task.deadline_convert),
        rx.table.cell(rx.button("取消"), on_click=TaskTableState.cancel(task)),
    )


def task_table() -> rx.Component:
    return rx.vstack(
        rx.input(
            rx.input.slot(
                rx.icon(tag="search"),
            ),
            default_value=TaskTableState.search_value,
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
                        rx.table.column_header_cell("取消"),
                    ),
                ),
                rx.table.body(
                    rx.foreach(TaskTableState.comp_tasks, show_task),
                ),
                on_mount=TaskTableState.comp_load_entries,
            ),
            type="auto",
            scrollbars="vertical",
            height="15em",
        ),
    )
