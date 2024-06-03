import reflex as rx

from ene_backend import styles


def icon_dialog(dialog: tuple[str, str]) -> rx.Component:
    """Create a dialog box with icons.

    Args:
        dialog: A pair of user message and system response.

    Returns:
        The dialog box component.
    """
    user_message, system_response = dialog
    return rx.vstack(
        rx.box(
            rx.markdown(
                user_message,
                background_color=rx.color("mint", 4),
                **styles.message_style,
            ),
            text_align="right",
            align_self="flex-end",
            max_width="80%",
            _hover={"transform": "scale(1.1)"},
        ),
        rx.box(
            rx.markdown(
                system_response,
                background_color=rx.color("gray", 5),
                **styles.message_style,
            ),
            text_align="left",
            padding_top="1em",
            align_self="flex-start",
            max_width="80%",
            _hover={"transform": "scale(1.1)"},
        ),
        width="inherit",
        padding_x="1em",
        justify="between",
        align="stretch",
        spacing="2",
        _hover={"background": "cyan"},
    )
