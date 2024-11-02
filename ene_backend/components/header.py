import asyncio
from datetime import datetime

import reflex as rx

from ene_backend import styles

from ..state.auth import AuthState
from ..state.chat_state import ChatState


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


class DialogState(rx.State):
    dialog_open: bool = False

    def set_dialog_open(self, value: bool):
        self.dialog_open = value


def logout_dialog():
    return rx.alert_dialog.root(
        rx.alert_dialog.content(
            rx.alert_dialog.title("ログアウトしますか？"),
            rx.flex(
                rx.alert_dialog.cancel(rx.button("キャンセル", color_scheme="gray")),
                rx.alert_dialog.action(
                    rx.button(
                        "ログアウト",
                        color_scheme="red",
                        on_click=[
                            ChatState.reflesh,
                            AuthState.logout,
                        ],
                    ),
                ),
                spacing="3",
                margin_top="16px",
                justify="end",
            ),
            style={"width": "300px"},
        ),
        open=DialogState.dialog_open,
        on_open_change=DialogState.set_dialog_open(False),
    )


def navi_bar() -> rx.Component:
    """Navigation bar for each page of the app.

    Returns:
        The navigation bar component.
    """

    return rx.box(
        rx.hstack(
            # Logo (tentative)
            rx.image(
                src="/logo.png",
                height="3em",
                width="auto",
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
                    AuthState.name,  # tentative
                    font_size="2em",
                    color=rx.color_mode_cond("white", "black"),
                ),
                rx.spacer(),
                rx.menu.root(
                    rx.menu.trigger(
                        rx.button(
                            rx.icon(tag="settings"),
                            variant="solid",
                            size="4",
                            color_scheme="iris",
                            border_radius=styles.border_radius,
                        ),
                    ),
                    rx.menu.content(
                        rx.menu.item("プロフィールを編集", on_click=rx.redirect("/user_profile")),
                        rx.menu.item("ログアウト", on_click=DialogState.set_dialog_open(True), color="red"),
                    ),
                ),
                logout_dialog(),
                aline="center",
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
