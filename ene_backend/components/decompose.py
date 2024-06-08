import reflex as rx

from ene_backend import styles

from ..state.task_state import TaskTableState


class DecomposeTaskState(rx.State):
    original_task: str = "AIで分解"
    decomposed_tasks: list = []

    def change_original_task(self, original_task: str):
        self.original_task = original_task
        self.decomposed_tasks = [
            "new " + original_task,
            "further " + original_task,
            "supreme " + original_task,
            "Sikanoko " + original_task,
            "Final " + original_task,
        ]


def task_box(task_name: str) -> rx.Component:
    return rx.box(
        rx.text(task_name, text_align="center"),
        background=rx.color("iris"),
        width="100%",
        padding_y="1em",
        justify="between",
        align="start",
        border_radius=styles.border_radius,
        _hover={"transform": "scale(1.1)"},
    )


def lined_task_box(task_list: list) -> rx.Component:
    return rx.grid(rx.foreach(task_list, task_box), width="100%", columns="5", spacing="4", justify="start")


def decomposed_task_box() -> rx.Component:
    return rx.vstack(
        rx.hstack(
            rx.text("あなたのタスクを分解しましょう", size="7"),
            rx.dialog.root(
                rx.dialog.trigger(
                    rx.button(
                        rx.text(DecomposeTaskState.original_task, text_align="center"),
                        background=rx.color("blue"),
                        width="30%",
                        height="100%",
                        padding_y="1em",
                        justify="between",
                        align="start",
                        border_radius=styles.border_radius,
                        _hover={"transform": "scale(1.1)"},
                    ),
                ),
                rx.dialog.content(
                    rx.form(
                        rx.dialog.title("タスクの因数分解"),
                        rx.vstack(
                            rx.grid(
                                rx.foreach(
                                    TaskTableState.tasks,
                                    lambda task: rx.button(
                                        f"{task.name}",
                                        on_click=DecomposeTaskState.change_original_task(f"{task.name}"),
                                    ),
                                ),
                                width="100%",
                                columns="4",
                                spacing="5",
                            )
                        ),
                    )
                ),
            ),
            align="center",
            justify="between",
        ),
        lined_task_box(DecomposeTaskState.decomposed_tasks),
        width="inherit",
        height="inherit",
        padding="1em",
        justify="between",
        align="stretch",
    )
