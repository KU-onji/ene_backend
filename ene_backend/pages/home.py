import reflex as rx

from ene_backend.components import calendar, icon_dialog, suggestion
from ene_backend.templates import template


def content_field(width: str, height: str, *contents: rx.Component) -> rx.Component:
    return rx.box(
        rx.vstack(
            *contents,
            spacing="2",
            width="inherit",
            height="inherit",
            align="start",
            justify="start",
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
            content_field("100%", "60%", suggestion.suggestion()),
            content_field("100%", "40%", calendar.calendar()),
            justify="center",
            align="center",
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
