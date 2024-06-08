import asyncio
from datetime import datetime

import reflex as rx

from ene_backend import styles


class CurrentTimeState(rx.State):
    current_date: str = datetime.now().strftime("%Y/%m/%d")
    current_time: str = datetime.now().strftime("%H:%M:%S")

    @rx.cached_var
    def time_info(self):
        ctime = self.current_time
        return ctime

    def refresh(self):
        self.current_date = datetime.now().strftime("%Y/%m/%d")
        self.current_time = datetime.now().strftime("%H:%M:%S")

    # To be implemented
    @rx.background
    async def update_time(self):
        while True:
            async with self:
                self.refresh()
            await asyncio.sleep(1)

    # def on_load(self):
    #    return self.refresh()


def navi_bar() -> rx.Component:
    """Navigation bar for each page of the app.

    Returns:
        The navigation bar component.
    """
    return rx.box(
        rx.hstack(
            # Logo (tentative)
            rx.box(
                rx.text("ene", font_size="2em", color="iris", align="center"),
                padding_x="1em",
                border_radius=styles.border_radius,
                background=rx.color_mode_cond("lightgray", "black"),
            ),
            # Clock (to be implemented)
            rx.center(
                rx.heading(
                    CurrentTimeState.current_date,
                    font_size="2em",
                    color_scheme=rx.color_mode_cond("black", "lightgray"),
                ),
                background=rx.color_mode_cond("lightgray", "black"),
                padding="0.5em",
                border_radius=styles.border_radius,
            ),
            rx.center(
                rx.heading(
                    CurrentTimeState.current_time,
                    font_size="2em",
                    color_scheme=rx.color_mode_cond("black", "lightgray"),
                ),
                background=rx.color_mode_cond("lightgray", "black"),
                padding="0.5em",
                border_radius=styles.border_radius,
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
                    size="md",
                    on_click=rx.redirect("/user_profile"),
                    color_scheme="iris",
                    border_radius=styles.border_radius,
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
