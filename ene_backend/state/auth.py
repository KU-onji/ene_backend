from typing import Optional

import reflex as rx
from sqlmodel import select

from ..db_model import User


class ThemeState(rx.State):
    """The state for the theme of the app."""

    accent_color: str = "crimson"

    gray_color: str = "gray"
    user: Optional[User] = None

    def check_login(self):
        if not self.logged_in:
            return rx.redirect("/")

    @rx.var
    def logged_in(self):
        return self.user is not None


class AuthState(ThemeState):
    address: str
    password: str
    confirm_password: str
    name: str | None

    def get_address(self):
        return self.address

    def signup(self):
        with rx.session() as session:
            if self.password != self.confirm_password:
                return rx.window_alert("確認用のパスワードが一致しません")
            if session.exec(select(User).where(User.address == self.address)).first():
                return rx.window_alert("すでに登録されているメールアドレスです")
            self.user = User(address=self.address, password=self.password)
            session.add(self.user)
            session.expire_on_commit = False
            session.commit()
            return rx.redirect("/")

    def login(self):
        print(type(User.address))
        print(type(self.address))
        with rx.session() as session:
            user = session.exec(select(User).where(User.address == self.address)).first()
            if user and user.password == self.password:
                self.user = user
                return rx.redirect("/home")
            else:
                return rx.window_alert("ユーザー名またはパスワードが正しくありません。")

    # update user profile
    def update_profile(self, profile: dict):
        with rx.session() as session:
            user = session.exec(select(User).where(User.address == self.address)).first()
            if user and user.password == profile["password"]:
                if profile["address"] != "":
                    self.address = profile["address"]
                    user.address = self.address
                if profile["name"] != "":
                    self.name = profile["name"]
                    user.name = self.name
                session.expire_on_commit = False
                session.commit()
            else:
                return rx.window_alert("パスワードが正しくありません。")
