import json
import os
import re
import time
from typing import Optional

import bcrypt
import reflex as rx
from google.auth.transport import requests
from google.oauth2.id_token import verify_oauth2_token
from sqlmodel import select

from ..db_model import User

CLIENT_ID = os.getenv("GOOGLE_CLIENT_ID")


class ThemeState(rx.State):
    """The state for the theme of the app."""

    accent_color: str = "crimson"

    gray_color: str = "gray"
    user: Optional[User] = None
    id_token_json: str = rx.LocalStorage()

    def check_login(self):
        if not self.logged_in:
            self.id_token_json = ""
            self.user = None
            return rx.redirect("/")

    @rx.var(cache=True)
    def tokeninfo(self) -> dict[str, str]:
        if not self.id_token_json:
            return {}

        try:
            id_info = verify_oauth2_token(
                json.loads(self.id_token_json)["credential"],
                requests.Request(),
                CLIENT_ID,
            )
            if id_info["aud"] != CLIENT_ID:
                raise ValueError("Invalid audience.")
            return id_info
        except ValueError as exc:
            print(f"Error verifying token: {exc}")
        return {}

    @rx.var
    def token_is_valid(self) -> bool:
        try:
            if self.tokeninfo and int(self.tokeninfo.get("exp", 0)) > time.time():
                return True
            else:
                return False
        except Exception:
            return False

    @rx.var
    def logged_in(self):
        return self.user is not None or self.token_is_valid


class AuthState(ThemeState):
    address: str
    password: str
    confirm_password: str
    name: str
    user_id: str

    def signup_submit(self, form_data: dict):
        self.address = form_data["address"]
        self.password = form_data["password"]
        self.confirm_password = form_data["confirm_password"]
        self.name = form_data["name"]
        return self.signup()

    def login_submit(self, form_data: dict):
        self.address = form_data["address"]
        self.password = form_data["password"]
        return self.login()

    def is_valid_email(self, email: str) -> bool:
        return bool(re.match(r"[^@]+@[^@]+\.[^@]+", email))

    def signup(self):
        with rx.session() as session:
            if not self.is_valid_email(self.address):
                self.reset()
                return rx.window_alert("メールアドレスの形式が正しくありません")
            if self.password != self.confirm_password:
                self.reset()
                return rx.window_alert("確認用のパスワードが一致しません")
            if session.exec(select(User).where(User.address == self.address)).first():
                self.reset()
                return rx.window_alert("このメールアドレスは利用できません")
            self.user = User(
                address=self.address,
                password=bcrypt.hashpw(self.password.encode("utf-8"), bcrypt.gensalt()),
                name=self.name,
            )
            session.add(self.user)
            session.expire_on_commit = False
            session.commit()
            return rx.redirect("/home")

    def login(self):
        with rx.session() as session:
            user = session.exec(select(User).where(User.address == self.address)).first()
            if user and bcrypt.checkpw(self.password.encode("utf-8"), user.password.encode("utf-8")):
                self.user = user
                self.user_id = user.id
                self.name = user.name
                return rx.redirect("/home")
            else:
                self.reset()
                return rx.window_alert("メールアドレスまたはパスワードが正しくありません。")

    def logout(self):
        self.reset()
        return rx.redirect("/")

    # update user profile
    def update_profile(self, profile: dict):
        with rx.session() as session:
            user = session.exec(select(User).where(User.address == self.address)).first()
            if profile["address"] != "":
                self.address = profile["address"]
                user.address = self.address
            if profile["name"] != "":
                self.name = profile["name"]
                user.name = self.name
            session.expire_on_commit = False
            session.commit()
            return rx.redirect("/home")

    def on_success_login(self, id_token: dict):
        self.id_token_json = json.dumps(id_token)
        self.address = self.tokeninfo["email"]
        self.name = self.tokeninfo["name"]
        self.password = self.tokeninfo["sub"]
        return self.login()

    def on_success_signup(self, id_token: dict):
        self.id_token_json = json.dumps(id_token)
        self.address = self.tokeninfo["email"]
        self.name = self.tokeninfo["name"]
        self.password = self.tokeninfo["sub"]
        self.confirm_password = self.tokeninfo["sub"]
        return self.signup()
