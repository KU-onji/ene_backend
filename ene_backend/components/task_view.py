import reflex as rx

from ene_backend import styles


class TaskState(rx.State):
    name: list[str] = ["Task 1", "Task 2", "Task 3", "Task 4", "Task 5"]
    priority: list[str] = ["High", "Middle", "Low", "High", "Middle"]

    def add_task(self, task: str, priority: str) -> None:
        self.name.append(task)
        self.priority.append(priority)

    def remove_task(self, task: str) -> None:
        task_index = self.name.index(task)
        self.name.pop(task_index)
        self.priority.pop(task_index)


def task_view() -> rx.Component:
    def card_color(priority: rx.Var) -> str:
        return rx.cond(
            priority == "High",
            "tomato",
            rx.cond(priority == "Middle", "mint", "iris"),
        )

    def task_card(name: str, priority: str) -> rx.Component:
        return rx.popover.root(
            rx.popover.trigger(
                rx.button(
                    name,
                    size="4",
                    color_scheme=card_color(priority),
                    variant="solid",
                    border_radius=styles.border_radius,
                ),
            ),
            rx.popover.content(
                rx.flex(
                    rx.text(f"Priority: {priority}"),
                    rx.popover.close(
                        rx.button(
                            "Delete",
                            on_click=TaskState.remove_task(name),
                            color_scheme="tomato",
                            variant="solid",
                            border_radius=styles.border_radius,
                        ),
                        rx.button(
                            "Edit",
                            on_click=TaskState.remove_task(name),
                            color_scheme="mint",
                            variant="solid",
                            border_radius=styles.border_radius,
                        ),
                        rx.button(
                            "Close",
                            color_scheme="iris",
                            variant="solid",
                            border_radius=styles.border_radius,
                        ),
                    ),
                ),
                side="bottom",
            ),
        )

    return rx.flex(
        rx.foreach(
            TaskState.name,
            lambda name: rx.foreach(
                TaskState.priority,
                lambda priority: task_card(name, priority),
            ),
        ),
        spacing="2",
        wrap="wrap",
        width="100%",
        height="100%",
        padding="1em",
        align="start",
        justify="between",
    )
