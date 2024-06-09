import reflex as rx

from ene_backend import styles

from ..state.task_state import TaskTableState


class DecomposeTaskState(rx.State):
    original_task: str = "AIで分解"
    selected_task: str = ""

    def change_original_task(self, original_task: str):
        self.original_task = original_task

    def set_selected_task(self, value: str):
        self.selected_task = value

    def reflect_selected_task(self):
        self.change_original_task(self.selected_task)

    @rx.var
    def decomposed_tasks(self) -> list[str]:
        def decomposed_task_list(task_name: str) -> list[str]:
            return (
                []
                if task_name == "AIで分解"
                else [
                    "new " + task_name,
                    "further " + task_name,
                    "supreme " + task_name,
                    "Sikanoko " + task_name,
                    "Final " + task_name,
                ]
            )

        return decomposed_task_list(self.original_task)

    @rx.var
    def too_long_task_name(self) -> bool:
        return len(self.original_task) >= 20


def task_box(task_name: str) -> rx.Component:
    return rx.box(
        rx.text(task_name, text_align="center"),
        background=rx.color("iris"),
        width="100%",
        padding_y="1em",
        justify="between",
        align="start",
        border_radius=styles.border_radius,
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
                        rx.cond(
                            DecomposeTaskState.too_long_task_name,
                            rx.text(DecomposeTaskState.original_task[0:20] + "...", text_align="center"),
                            rx.text(DecomposeTaskState.original_task, text_align="center"),
                        ),
                        background=rx.color("blue"),
                        width="40%",
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
                        rx.form.root(
                            rx.vstack(
                                rx.select(
                                    TaskTableState.str_task_list,
                                    name="selected_task",
                                    variant="soft",
                                    radius="full",
                                    width="100%",
                                    on_change=DecomposeTaskState.set_selected_task,
                                ),
                                rx.button("Decompose", on_click=DecomposeTaskState.reflect_selected_task),
                            ),
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
