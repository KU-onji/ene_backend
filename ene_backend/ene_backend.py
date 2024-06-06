"""Welcome to Reflex!."""

# Import all the pages.
import reflex as rx

from ene_backend.pages import add_task, home, login, settings, signup

add_task
settings
home.home
login
signup


class State(rx.State):
    """Define empty state to allow access to rx.State.router."""


# Create the app.
app = rx.App()
