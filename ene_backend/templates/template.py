"""Common templates used between pages in the app."""

from __future__ import annotations

from typing import Callable

import reflex as rx

from ene_backend import styles
from ene_backend.components.header import navi_bar

from ..state.auth import ThemeState

# Meta tags for the app.
default_meta = [
    {
        "name": "viewport",
        "content": "width=device-width, shrink-to-fit=no, initial-scale=1",
    },
]


def menu_item_link(text, href):
    return rx.menu.item(
        rx.link(
            text,
            href=href,
            width="100%",
            color="inherit",
        ),
        _hover={
            "color": styles.accent_color,
            "background_color": styles.accent_text_color,
        },
    )


def menu_button() -> rx.Component:
    """The menu button on the top right of the page.

    Returns:
        The menu button component.
    """
    from reflex.page import get_decorated_pages

    return rx.box(
        rx.menu.root(
            rx.menu.trigger(
                rx.button(
                    rx.icon("menu"),
                    variant="soft",
                )
            ),
            rx.menu.content(
                *[menu_item_link(page["title"], page["route"]) for page in get_decorated_pages()],
                rx.menu.separator(),
                menu_item_link("About", "https://github.com/reflex-dev"),
                menu_item_link("Contact", "mailto:founders@=reflex.dev"),
            ),
        ),
        position="fixed",
        right="2em",
        top="2em",
        z_index="500",
    )


def template(
    route: str | None = None,
    title: str | None = None,
    description: str | None = None,
    meta: str | None = None,
    navi: bool = True,
    script_tags: list[rx.Component] | None = None,
    on_load: rx.event.EventHandler | list[rx.event.EventHandler] | None = None,
) -> Callable[[Callable[[], rx.Component]], rx.Component]:
    """The template for each page of the app.

    Args:
        route: The route to reach the page.
        title: The title of the page.
        description: The description of the page.
        meta: Additionnal meta to add to the page.
        on_load: The event handler(s) called when the page load.
        script_tags: Scripts to attach to the page.

    Returns:
        The template with the page content.
    """

    def decorator(page_content: Callable[[], rx.Component]) -> rx.Component:
        """The template for each page of the app.

        Args:
            page_content: The content of the page.

        Returns:
            The template with the page content.
        """
        # Get the meta tags for the page.
        all_meta = [*default_meta, *(meta or [])]

        def templated_page():
            return rx.vstack(
                navi_bar(),
                rx.box(
                    rx.vstack(
                        page_content(),
                        width="100%",
                        height="100%",
                        **styles.template_content_style,
                    ),
                    width="100%",
                    height="calc(100vh - 7em)",
                    **styles.template_page_style,
                ),
                # menu_button(),
                background=f"radial-gradient(circle at top right, {rx.color('accent', 2)}, {rx.color('mauve', 1)});",
                position="relative",
                width="100%",
                height="100vh",
            )

        def no_navi_page():
            return rx.vstack(
                rx.box(
                    rx.vstack(
                        page_content(),
                        width="100%",
                        height="100%",
                        **styles.template_content_style,
                    ),
                    width="100%",
                    height="calc(100vh - 7em)",
                    **styles.template_page_style,
                ),
                # menu_button(),
                background=f"radial-gradient(circle at top right, {rx.color('accent', 2)}, {rx.color('mauve', 1)});",
                position="relative",
                width="100%",
                height="100vh",
            )

        @rx.page(
            route=route,
            title=title,
            description=description,
            meta=all_meta,
            script_tags=script_tags,
            on_load=on_load,
        )
        def theme_wrap():
            if navi:
                return rx.theme(
                    templated_page(),
                    has_background=True,
                    accent_color=ThemeState.accent_color,
                    gray_color=ThemeState.gray_color,
                )
            else:
                return rx.theme(
                    no_navi_page(),
                    has_background=True,
                    accent_color=ThemeState.accent_color,
                    gray_color=ThemeState.gray_color,
                )

        return theme_wrap

    return decorator
