import reflex as rx


def content_tab(*content_and_name: tuple[rx.Component, str]) -> rx.Component:
    contents, names = zip(*content_and_name)
    return rx.tabs.root(
        rx.tabs.list(*[rx.tabs.trigger(name, value=f"tab_{name}") for name in names]),
        *[
            rx.tabs.content(
                content,
                value=f"tab_{name}",
                height="calc(100% - 2.5em)",
            )
            for content, name in zip(contents, names)
        ],
        default_value=f"tab_{names[0]}",
        # height="100%",
        flex_grow="1",
    )
