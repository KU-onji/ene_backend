"""Welcome to Reflex! This file outlines the steps to create a basic app."""

import reflex as rx

from ene_backend.state.auth import AuthState
from ene_backend.templates import template
from ene_backend.templates.template import ThemeState


@template(route="/user_profile", title="プロフィール", on_load=ThemeState.check_login())
def profile() -> rx.Component:
    return rx.container(
        rx.color_mode.button(position="top-right"),
        rx.vstack(
            rx.heading("プロフィール", size="9"),
            rx.form(
                rx.vstack(
                    rx.hstack(
                        rx.text(
                            "E-mail: ",
                            size="5",
                        ),
                        rx.text(
                            AuthState.address,
                            size="5",
                        ),
                    ),
                    rx.input(
                        placeholder="新しいメールアドレス",
                        name="address",
                    ),
                    rx.hstack(
                        rx.text(
                            "ニックネーム: ",
                            size="5",
                        ),
                        rx.text(
                            AuthState.name,
                            size="5",
                        ),
                    ),
                    rx.input(
                        placeholder="新しいニックネーム",
                        name="name",
                    ),
                    rx.button("適用", width="10em", type="submit"),
                    rx.button("キャンセル", width="10em", variant="soft", on_click=rx.redirect("/home")),
                ),
                on_submit=AuthState.update_profile,
                reset_on_submit=True,
            ),
            spacing="5",
            justify="center",
            min_height="85vh",
        ),
    )
