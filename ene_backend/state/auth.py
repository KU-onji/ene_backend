import reflex as rx
from sqlmodel import select

from ene_backend.templates.template import ThemeState, User


class AuthState(ThemeState):
    address: str
    password: str
    confirm_password: str
    name: str

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
            if profile["address"] != "":
                self.address = profile["address"]
                user.address = self.address
            if profile["password"] != "":
                self.password = profile["password"]
                user.password = self.password
            if profile["name"] != "":
                self.name = profile["name"]
                user.name = self.name
            session.expire_on_commit = False
            session.commit()
