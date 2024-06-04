# from typing import Literal

import reflex as rx

from ene_backend import styles


def plan_suggestion() -> rx.Component:
    return rx.hstack(
        rx.box(
            rx.markdown(
                "こんなプランはどう？",
                background_color=rx.color("iris", 4),
                **styles.message_style,
            ),
            text_align="center",
            align_self="flex-start",
            max_width="80%",
            _hover={"transform": "scale(1.1)"},
        ),
        rx.box(
            rx.text(
                "ETA: 18h",
                background_color=rx.color("iris", 4),
                text_align="center",
                **styles.message_style,
            ),
            text_align="center",
            padding_x="1em",
            align_self="flex-end",
            _hover={"transform": "scale(1.1)"},
        ),
        width="inherit",
        padding="1em",
        justify="between",
        align="start",
    )


def draw_graph() -> rx.Component:
    class Task(rx.State):
        tasks: tuple[str, str, str, str] = [
            ("Task1", "2024-06-04-00-30", "2024-06-04-01-00", "middle"),
            ("Task2", "2024-06-04-01-30", "2024-06-04-10-00", "high"),
            ("Task3", "2024-06-04-13-00", "2024-06-04-15-00", "low"),
            ("Task4", "2024-06-04-18-40", "2024-06-04-21-30", "high"),
        ]

    def task_box(task: Task) -> rx.Component:
        return rx.box(
            rx.text(task[0], text_align="center"),
            background=rx.cond(
                task[3] == "high",
                rx.color("ruby", 5),
                rx.cond(
                    task[3] == "middle",
                    rx.color("mint", 5),
                    rx.color("iris", 5),
                ),
            ),
            width="50%",
            padding_y="1em",
            justify="between",
            align="start",
            border_radius=styles.border_radius,
            _hover={"transform": "scale(1.1)"},
        )

    return rx.hstack(
        rx.foreach(Task.tasks, task_box),
        width="inherit",
        justify="between",
        align="center",
        _hover={"background": "cyan"},
    )


def suggestion() -> rx.Component:
    return rx.vstack(
        plan_suggestion(),
        draw_graph(),
        width="inherit",
        height="inherit",
        padding="1em",
        justify="between",
        align="center",
    )
