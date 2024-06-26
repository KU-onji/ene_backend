"""Styles for the app."""

import reflex as rx

border_radius = "0.375rem"
border = f"1px solid {rx.color('gray', 6)}"
text_color = rx.color("gray", 11)
accent_text_color = rx.color("accent", 10)
accent_color = rx.color("accent", 1)
hover_accent_color = {"_hover": {"color": accent_text_color}}
hover_accent_bg = {"_hover": {"background_color": accent_color}}
content_width_vw = "90vw"
sidebar_width = "20em"

template_page_style = {
    "padding_top": "7em",
    "flex": "1",
}

template_content_style = {
    "border_radius": border_radius,
    "min_height": "90vh",
    # "overflow": "auto",
    "align": "center",
    "justify": "center",
    "position": "relative",
}

link_style = {
    "color": accent_text_color,
    "text_decoration": "none",
    **hover_accent_color,
}

overlapping_button_style = {
    "background_color": "white",
    "border_radius": border_radius,
}

markdown_style = {
    "code": lambda text: rx.code(text, color_scheme="gray"),
    "codeblock": lambda text, **props: rx.code_block(text, **props, margin_y="1em"),
    "a": lambda text, **props: rx.link(
        text,
        **props,
        font_weight="bold",
        text_decoration="underline",
        text_decoration_color=accent_text_color,
    ),
}

header_style = {
    "position": "fixed",
    "padding": "1em 2em",
    "width": "100%",
    "height": "13ex",
    "top": "0px",
    "z_index": "500",
}

message_style = {
    "display": "inline-block",
    "padding_x": "1em",
    "border_radius": border_radius,
}

graph_style = {"background_color": rx.color("cyan", 4), **message_style}

button_box_style = {
    "variant": "soft",
    "font_size": "1.25em",
    "width": "100%",
    "height": "20%",
    "padding_y": "1em",
    "border_radius": border_radius,
}
