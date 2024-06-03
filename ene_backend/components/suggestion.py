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
    pass


def suggestion() -> rx.Component:
    return rx.vstack(
        plan_suggestion(),
        draw_graph(),
        width="inherit",
        padding="1em",
        justify="between",
        align="center",
    )
