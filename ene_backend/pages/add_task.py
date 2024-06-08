"""Add task page."""

import reflex as rx

# from ene_backend.templates import template


# @template(route="/add_task", title="Add Task")
def add_task() -> rx.Component:
    """Add task page.

    Returns:
        The UI for Add task page.
    """
    return rx.vstack(
        rx.heading("タスクを追加", size="8"),
        rx.dialog.root(
            rx.dialog.trigger(rx.button("タスクを追加")),
            rx.dialog.content(
                rx.form(
                    rx.dialog.title("タスクを追加"),
                    rx.flex(
                        rx.text("名前:"),
                        rx.input(name="name", required=True),
                        rx.text("優先度"),
                        rx.select(["低", "中", "高"], default_value="高", name="priority"),
                        rx.text("カテゴリ"),
                        rx.input(name="category"),
                        rx.text("締切日時:"),
                        rx.input(name="deadline", type="datetime-local", required=True),
                        rx.text("詳細:"),
                        rx.text_area(name="memo"),
                        direction="column",
                        spacing="3",
                    ),
                    rx.flex(
                        rx.dialog.close(
                            rx.button(
                                "キャンセル",
                                color_scheme="gray",
                                variant="soft",
                            ),
                        ),
                        rx.dialog.close(
                            rx.button("追加", type="submit"),
                        ),
                        spacing="3",
                        margin_top="16px",
                        justify="end",
                    ),
                ),
            ),
        ),
    )
