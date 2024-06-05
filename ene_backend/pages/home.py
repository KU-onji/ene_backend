from typing import Literal

import reflex as rx

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
        background=rx.color_mode_cond("white", "black"),
        width=width,
        height=height,
        # _hover={"background": "tomato"},  # for debugging
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
        background=rx.color_mode_cond("lightgray", "darkgray"),
        padding_y="1em",
        padding_left="1em",
        width="55%",
    )


def right_box() -> rx.Component:
    return rx.box(
        content_field(
            "100%",
            "90%",
            "start",
            "start",
            icon_dialog.icon_dialog(("Hello", "Hi")),
            icon_dialog.icon_dialog(("How are you?", "I'm fine.")),
        ),
        background=rx.color_mode_cond("lightgray", "darkgray"),
        padding="1em",
        width="45%",
    )


def task_add_button() -> rx.Component:
    """The button to add a task.

    Returns:
        The button to add a task.
    """
    return rx.button(
        rx.icon("plus", size=100),
        on_click=rx.redirect("/home"),
        color_scheme="iris",
        variant="solid",
        border_radius="50%",
        draggable=True,
        width="7em",
        height="7em",
        position="fixed",
        left="2em",
        bottom="2em",
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
            task_add_button(),
            spacing="0",
            width="100%",
            height="100%",
            align="stretch",
        ),
        width="100vw",
        height="calc(100vh - 7em)",
    )
