"""Welcome to Reflex!."""

# Import all the pages.
import reflex as rx

from ene_backend.pages import dashboard, index, login, settings, signup

dashboard
index
settings
login
signup


class State(rx.State):
    """Define empty state to allow access to rx.State.router."""


# Create the app.
app = rx.App()
