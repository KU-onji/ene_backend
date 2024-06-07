import reflex as rx


class User(rx.Model, table=True):
    address: str
    password: str
    name: str
