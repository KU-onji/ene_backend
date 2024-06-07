"""Welcome to Reflex!."""

# Import all the pages.
import reflex as rx

from ene_backend.pages import home, login, settings, signup, user_profile

settings
home.home
login
signup
user_profile


class State(rx.State):
    """Define empty state to allow access to rx.State.router."""


# Create the app.
app = rx.App()
