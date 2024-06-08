import reflex as rx

from ene_backend import styles


def icon_dialog(user_message: str, system_response: str) -> rx.Component:
    """Create a dialog box with icons.

    Args:
        user_message: The message from the user.
        system_response: The response from the system.

    Returns:
        The dialog box component.
    """
    return rx.vstack(
        rx.box(
            rx.text(
                user_message,
                background_color=rx.color("mint", 4),
                **styles.message_style,
            ),
            text_align="right",
            align_self="flex-end",
            max_width="80%",
            # _hover={"transform": "scale(1.1)"},
        ),
        rx.hstack(
            rx.avatar(
                src="/assistant_icon.png",
                size="4",
                radius="full",
            ),
            rx.box(
                rx.text(
                    system_response,
                    background_color=rx.color("gray", 5),
                    **styles.message_style,
                ),
                text_align="left",
                padding_top="1em",
                align_self="flex-start",
                max_width="80%",
                # _hover={"transform": "scale(1.1)"},
            ),
        ),
        width="inherit",
        padding_x="1em",
        justify="between",
        align="stretch",
        spacing="2",
        margin_bottom="1em",
        # _hover={"background": "cyan"},  # for debugging
    )
