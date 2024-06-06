import reflex as rx
from sqlmodel import select

from ene_backend.templates.template import ThemeState, User


class AuthState(ThemeState):
    address: str
    password: str
    confirm_password: str

    def signup(self):
        with rx.session() as session:
            if self.password != self.confirm_password:
                return rx.window_alert("Passwords do not match")
            if session.exec(select(User).where(User.address == self.address)).first():
                return rx.window_alert("Address already exists")
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
                return rx.redirect("/ene-home")
            else:
                return rx.window_alert("ユーザー名またはパスワードが正しくありません。")
