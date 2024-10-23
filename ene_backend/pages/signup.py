"""The Login Page"""

import os

import reflex as rx

from ene_backend.state.auth import AuthState
from ene_backend.templates import template

from ..react_oauth_google import GoogleLogin, GoogleOAuthProvider

CLIENT_ID = os.getenv("GOOGLE_CLIENT_ID")


@template(route="/signup", title="サインアップ", navi=False)
def signup_single_thirdparty() -> rx.Component:
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
                        "アカウントを作成",
                        size="6",
                        as_="h2",
                        text_align="left",
                        width="100%",
                    ),
                    rx.hstack(
                        rx.text(
                            "すでにアカウントをお持ちですか？",
                            size="3",
                            text_align="left",
                        ),
                        rx.link("サインイン", href="/", size="3"),
                        spacing="2",
                        opacity="0.8",
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
                    rx.text(
                        "ユーザー名",
                        size="3",
                        weight="medium",
                        text_align="left",
                        width="100%",
                    ),
                    rx.input(
                        rx.input.slot(rx.icon("smile")),
                        placeholder="ユーザー名",
                        on_blur=AuthState.set_name,
                        type="name",
                        size="3",
                        width="100%",
                    ),
                    justify="start",
                    spacing="2",
                    width="100%",
                ),
                rx.vstack(
                    rx.text(
                        "パスワード",
                        size="3",
                        weight="medium",
                        text_align="left",
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
                    justify="start",
                    spacing="2",
                    width="100%",
                ),
                rx.vstack(
                    rx.text(
                        "パスワード（再入力）",
                        size="3",
                        weight="medium",
                        text_align="left",
                        width="100%",
                    ),
                    rx.input(
                        rx.input.slot(rx.icon("lock")),
                        placeholder="パスワード（再入力）",
                        on_blur=AuthState.set_confirm_password,
                        type="password",
                        size="3",
                        width="100%",
                    ),
                    justify="start",
                    spacing="2",
                    width="100%",
                ),
                # rx.box(
                #     rx.checkbox(
                #         "利用規約に同意しました",
                #         default_checked=True,
                #         spacing="2",
                #     ),
                #     width="100%",
                # ),
                rx.button("新規登録", on_click=AuthState.signup, size="3", width="100%"),
                rx.hstack(
                    rx.divider(margin="0"),
                    rx.text(
                        "他のアカウントで新規登録",
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
                            GoogleLogin.create(on_success=AuthState.on_success_signup),
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
            max_width="28em",
            width="100%",
        ),
        opacity="0.8",
        width="100%",
    )
