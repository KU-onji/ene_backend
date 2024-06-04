"""Add task page."""

import reflex as rx

from ene_backend.templates import template


@template(route="/add_task", title="Add Task")
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
                rx.dialog.title("タスクを追加"),
                rx.flex(
                    rx.text("名前:"),
                    rx.input(),
                    rx.text("締切日時:"),
                    rx.input(type="datetime-local"),
                    rx.text("詳細:"),
                    rx.text_area(),
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
                        rx.button("追加"),
                    ),
                    spacing="3",
                    margin_top="16px",
                    justify="end",
                ),
            ),
        ),
    )
