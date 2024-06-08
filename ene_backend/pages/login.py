"""The Login Page"""

import reflex as rx

from ene_backend.components.header import CurrentTimeState
from ene_backend.state.auth import AuthState
from ene_backend.templates import template


@template(route="/", title="ログイン", on_load=CurrentTimeState.update_time())
def login_single_thirdparty() -> rx.Component:
    return rx.center(
        rx.card(
            rx.vstack(
                rx.flex(
                    rx.image(
                        src="/task.jpg",
                        width="2.5em",
                        height="auto",
                        border_radius="25%",
                    ),
                    rx.heading(
                        "ログイン",
                        size="6",
                        as_="h2",
                        text_align="left",
                        width="100%",
                    ),
                    direction="column",
                    justify="start",
                    spacing="4",
                    width="100%",
                ),
                rx.vstack(
                    rx.text(
                        "メールアドレス",
                        size="3",
                        weight="medium",
                        text_align="left",
                        width="100%",
                    ),
                    rx.input(
                        rx.input.slot(rx.icon("mail")),
                        placeholder="メールアドレス",
                        on_blur=AuthState.set_address,
                        type="email",
                        size="3",
                        width="100%",
                    ),
                    justify="start",
                    spacing="2",
                    width="100%",
                ),
                rx.vstack(
                    rx.hstack(
                        rx.text(
                            "パスワード",
                            size="3",
                            weight="medium",
                        ),
                        rx.link(
                            "パスワードを忘れた場合",
                            href="#",
                            size="3",
                        ),
                        justify="between",
                        width="100%",
                    ),
                    rx.input(
                        rx.input.slot(rx.icon("lock")),
                        placeholder="パスワード",
                        on_blur=AuthState.set_password,
                        type="password",
                        size="3",
                        width="100%",
                    ),
                    spacing="2",
                    width="100%",
                ),
                rx.button("ログイン", size="3", width="100%", on_click=AuthState.login),
                rx.center(
                    rx.text(
                        "新規登録は",
                        size="3",
                        text_align="left",
                    ),
                    rx.link("こちら", href="/signup", size="3"),
                    opacity="0.8",
                    direction="row",
                    width="100%",
                ),
                rx.hstack(
                    rx.divider(margin="0"),
                    rx.text(
                        "他のアカウントでログイン",
                        white_space="nowrap",
                        weight="medium",
                    ),
                    rx.divider(margin="0"),
                    align="center",
                    width="100%",
                ),
                rx.button(
                    rx.image(
                        src="/google.jpg",
                        width="1.5em",
                        height="auto",
                        border_radius="25%",
                    ),
                    "Googleでログイン",
                    variant="outline",
                    size="3",
                    width="100%",
                ),
                spacing="6",
                width="100%",
            ),
            size="4",
            width="80%",
            max_width="28em",
        ),
        opacity="0.8",
        width="80%",
    )
