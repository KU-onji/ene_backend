from typing import Literal

import reflex as rx

from ene_backend import styles
from ene_backend.components import (
    content_tab,
    icon_dialog,
    my_calendar,
    suggestion,
    task_view,
)
from ene_backend.templates import template


def content_field(
    width: str,
    height: str,
    align: Literal["baseline", "center", "end", "start", "stretch"],
    justify: Literal["between", "center", "end", "start"],
    *contents: rx.Component,
) -> rx.Component:
    return rx.box(
        rx.vstack(
            *contents,
            spacing="2",
            width="100%",
            height="100%",
            align=align,
            justify=justify,
            # _hover={"background": "green"},  # for debugging
        ),
        border_radius="0.5em",
        padding="1em",
        background=rx.color_mode_cond("white", "#333333"),
        width=width,
        height=height,
        # _hover={"background": "tomato"},  # for debugging
    )


def button_boxes() -> rx.Component:
    """The button to add a task.

    Returns:
        The button to add a task.
    """
    return rx.flex(
        rx.button(
            rx.icon("message_circle"),
            "ほめて！",
            color_scheme="mint",
            **styles.button_box_style,
        ),
        rx.button(
            rx.icon("lightbulb"),
            "それAIでどうにかならない？",
            color_scheme="jade",
            **styles.button_box_style,
        ),
        rx.button(
            rx.icon("trash-2"),
            "履歴をクリア",
            color_scheme="tomato",
            **styles.button_box_style,
        ),
        rx.button(
            rx.icon("plus"),
            "タスクを追加",
            color_scheme="iris",
            **styles.button_box_style,
        ),
        direction="column",
        width="100%",
        height="20%",
        justify="between",
        align="stretch",
        margin_top="1em",
    )


def left_box() -> rx.Component:
    return rx.box(
        rx.vstack(
            content_field("100%", "40%", "center", "between", suggestion.suggestion()),
            content_field(
                "100%",
                "60%",
                "stretch",
                "between",
                content_tab.content_tab(
                    (my_calendar.calendar_view(), "カレンダー"),
                    (task_view.task_view(), "タスク一覧"),
                ),
            ),
            justify="center",
            align="start",
            width="100%",
            height="100%",
        ),
        padding_y="1em",
        padding_left="1em",
        width="55%",
        height="100%",
    )


def right_box() -> rx.Component:
    return rx.flex(
        content_field(
            "100%",
            "80%",
            "start",
            "start",
            icon_dialog.icon_dialog(("Hello", "Hi")),
            icon_dialog.icon_dialog(("How are you?", "I'm fine.")),
        ),
        button_boxes(),
        direction="column",
        width="45%",
        height="100%",
        justify="center",
        align="center",
        padding="1em",
    )


@template(route="/home", title="ene: Home")
def home() -> rx.Component:
    """The home page.

    returns:
        The UI for the home page.
    """
    # full width background
    return rx.flex(
        rx.hstack(
            left_box(),
            right_box(),
            spacing="0",
            width="100%",
            height="100%",
            align="stretch",
        ),
        width="100vw",
        height="calc(100vh - 7em)",
        background=rx.color_mode_cond("#f0f0f0", "#666666"),
    )
