from typing import Literal

import reflex as rx

from ene_backend.components import icon_dialog, my_calendar, suggestion
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
            _hover={"background": "green"},
        ),
        border_radius="0.5em",
        padding="1em",
        background=rx.color_mode_cond("white", "black"),
        width=width,
        height=height,
        _hover={"background": "tomato"},
    )


def left_box() -> rx.Component:
    return rx.box(
        rx.vstack(
            content_field("100%", "40%", "center", "between", suggestion.suggestion()),
            content_field("100%", "60%", "stretch", "start", my_calendar.calendar_view()),
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
            "70%",
            "start",
            "start",
            icon_dialog.icon_dialog(("Hello", "Hi")),
            icon_dialog.icon_dialog(("How are you?", "I'm fine.")),
        ),
        background=rx.color_mode_cond("lightgray", "darkgray"),
        padding="1em",
        width="45%",
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
    )
