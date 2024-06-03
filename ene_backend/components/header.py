# import asyncio
from datetime import datetime

import reflex as rx

from ene_backend import styles


class CurrentTimeState(rx.State):
    current_date: str = datetime.now().strftime("%Y/%m/%d")
    current_time: str = datetime.now().strftime("%H:%M")

    def refresh(self):
        self.current_date = datetime.now().strftime("%Y/%m/%d")
        self.current_time = datetime.now().strftime("%H:%M")

    # To be implemented
    """ @rx.background
    async def update_time(self):
        while True:
            async with self:
                self.refresh()
            await asyncio.sleep(1) """

    def on_load(self):
        return self.refresh()


def navi_bar() -> rx.Component:
    """Navigation bar for each page of the app.

    Returns:
        The navigation bar component.
    """
    return rx.box(
        rx.hstack(
            # Logo (tentative)
            rx.color_mode_cond(
                rx.image(src="/reflex_white.svg", height="2em"),
                rx.image(src="/reflex_black.svg", height="2em"),
            ),
            # Clock (to be implemented)
            rx.center(
                rx.heading(
                    CurrentTimeState.current_time,
                    font_size="2em",
                    color_scheme=rx.color_mode_cond("black", "lightgray"),
                ),
                background=rx.color_mode_cond("lightgray", "black"),
                padding="0.5em",
                border_radius="0.5em",
            ),
            # UserName and config button
            rx.hstack(
                rx.text(
                    "KU-onji",  # tentative
                    font_size="2em",
                    color=rx.color_mode_cond("white", "black"),
                ),
                rx.spacer(),
                rx.button(
                    rx.icon(tag="settings"),
                    variant="solid",
                    size="4",
                    on_click=rx.redirect("/home"),
                    color_scheme="iris",
                ),
            ),
            align="center",
            justify="between",
            padding="1em 2em",
        ),
        background=rx.color_mode_cond(
            "rgba(15, 15, 15, 0.85)",
            "rgba(255, 255, 255, 0.85)",
        ),
        **styles.header_style,
    )
