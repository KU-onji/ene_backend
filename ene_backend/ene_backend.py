"""Welcome to Reflex!."""

# Import all the pages.
import reflex as rx

from ene_backend.pages import home, login, settings, signup

settings
home.home
login
signup


class State(rx.State):
    """Define empty state to allow access to rx.State.router."""


# Create the app.
app = rx.App()
