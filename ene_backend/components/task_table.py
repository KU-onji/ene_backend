import reflex as rx

from ..db_model import Task
from ..state.chat_state import ChatState
from ..state.task_state import TaskTableState


def show_task(task: Task):
    """Show a task in a table row."""
    return rx.table.row(
        rx.table.cell(
            rx.button(
                "完了",
                on_click=lambda: ChatState.answer(task),
            )
        ),
        rx.table.cell(task.name),
        rx.table.cell(task.priority),
        rx.table.cell(task.category),
        rx.table.cell(task.deadline_convert, color=task.color),
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
                            rx.hstack(
                                rx.text("名前"),
                                rx.text("【必須】", color_scheme="red"),
                                spacing="2",
                            ),
                            rx.input(name="name", default_value=task.name),
                            rx.hstack(
                                rx.text("優先度"),
                                rx.text("【必須】", color_scheme="red"),
                                spacing="2",
                            ),
                            rx.select(["低", "中", "高"], default_value=task.priority, name="priority"),
                            rx.hstack(
                                rx.text("優先度"),
                                rx.text("【任意】", color_scheme="gray"),
                                spacing="2",
                            ),
                            rx.input(name="category", default_value=task.category),
                            rx.hstack(
                                rx.text("締切日時"),
                                rx.text("【必須】", color_scheme="red"),
                                spacing="2",
                            ),
                            rx.input(name="deadline", type="datetime-local", default_value=task.deadline),
                            rx.hstack(
                                rx.text("所要時間"),
                                rx.text("【必須】", color_scheme="red"),
                                spacing="2",
                            ),
                            rx.hstack(
                                rx.input(name="hour", default_value=task.hour),
                                rx.text("時間"),
                                rx.input(name="minute", default_value=task.minute),
                                rx.text("分"),
                            ),
                            rx.hstack(
                                rx.text("メモ"),
                                rx.text("【任意】", color_scheme="gray"),
                                spacing="2",
                            ),
                            rx.text_area(
                                name="memo",
                                value=task.memo,
                                on_change=TaskTableState.set_memo,
                            ),
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
                                    "削除",
                                    color_scheme="red",
                                    variant="soft",
                                    type="reset",
                                    on_click=TaskTableState.delete_task,
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
                            spacing="3",
                            margin_top="16px",
                            justify="end",
                        ),
                        on_submit=TaskTableState.update_task,
                        reset_on_submit=True,
                    ),
                ),
            )
        ),
    )


def task_table() -> rx.Component:
    return rx.vstack(
        rx.flex(
            rx.input(
                rx.input.slot(
                    rx.icon(tag="search"),
                ),
                default_value=TaskTableState.search_value,
                placeholder="Search here...",
                on_change=lambda value: TaskTableState.filter_values(value),
            ),
            rx.icon(tag="arrow-down-narrow-wide"),
            rx.select(["日付", "優先度"], default_value="日付", on_change=TaskTableState.sort_values),
            spacing="2",
        ),
        rx.box(
            rx.scroll_area(
                rx.table.root(
                    rx.table.header(
                        rx.table.row(
                            rx.table.column_header_cell("完了"),
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
                height="100%",
                width="100%",
            ),
            height="100%",
            width="100%",
        ),
    )
