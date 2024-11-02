"""The Login Page"""

import os

import reflex as rx

from ene_backend.components.header import CurrentTimeState
from ene_backend.state.auth import AuthState
from ene_backend.templates import template

from ..react_oauth_google import GoogleLogin, GoogleOAuthProvider

CLIENT_ID = os.getenv("GOOGLE_CLIENT_ID")


@template(route="/", title="ログイン", on_load=CurrentTimeState.update_time())
def login_single_thirdparty() -> rx.Component:
    return rx.center(
        rx.card(
            rx.vstack(
                rx.flex(
                    rx.center(
                        rx.image(
                            src="/logo.png",
                            width="5em",
                            height="auto",
                            border_radius="25%",
                        ),
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
                rx.form(
                    rx.vstack(
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
                                name="address",
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
                                justify="between",
                                width="100%",
                            ),
                            rx.input(
                                rx.input.slot(rx.icon("lock")),
                                placeholder="パスワード",
                                name="password",
                                type="password",
                                size="3",
                                width="100%",
                            ),
                            spacing="2",
                            width="100%",
                        ),
                        rx.button("ログイン", size="3", width="100%", type="submit"),
                        justify="start",
                        spacing="4",
                        width="100%",
                    ),
                    on_submit=AuthState.login_submit,
                ),
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
                rx.vstack(
                    rx.center(
                        GoogleOAuthProvider.create(
                            GoogleLogin.create(on_success=AuthState.on_success_login),
                            client_id=CLIENT_ID,
                        ),
                    ),
                    width="100%",
                    align="center",
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
