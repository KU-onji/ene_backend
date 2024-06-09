import reflex as rx

from ene_backend import styles

from ..state.task_state import TaskTableState
from ..utils.gpt_utils import call_gpt, create_Client, create_partition_prompt


class DecomposeTaskState(rx.State):
    original_task: str = "分解するタスクを選択"
    selected_task: str = ""
    previous_task: str = "分解するタスクを選択"
    decomposed_task_list: list[str] = []

    def change_original_task(self, original_task: str):
        self.original_task = original_task

    def set_selected_task(self, value: str):
        self.selected_task = value

    def reflect_selected_task(self):
        self.change_original_task(self.selected_task)

    @rx.var
    def decomposed_tasks(self) -> list[str]:
        def decomposed_task_list(task_name: str) -> list[str]:
            client = create_Client()
            gpt_results = call_gpt(client, create_partition_prompt(task_name))
            # gpt_results = "(new task:1 hour),(new task2:30 min)"
            decomposed_list = gpt_results.split(",")
            task_name_list = []
            for task in decomposed_list:
                task_name, _ = task.split(":")
                task_name_list.append(task_name[1:])
            return task_name_list

        if self.previous_task != self.original_task:
            self.previous_task = self.original_task
            self.decomposed_task_list = decomposed_task_list(self.original_task)

        return self.decomposed_task_list

    @rx.var
    def too_long_task_name(self) -> bool:
        return len(self.original_task) >= 20


def task_box(task_name: str) -> rx.Component:
    return rx.dialog.root(
        rx.dialog.trigger(
            rx.button(
                rx.text(task_name, text_align="center"),
                background=rx.color("iris"),
                height="100%",
                width="100%",
                padding_y="1em",
                justify="between",
                align="start",
                border_radius=styles.border_radius,
            )
        ),
        rx.dialog.content(
            rx.form(
                rx.dialog.title("タスクを追加"),
                rx.flex(
                    rx.hstack(
                        rx.text("名前"),
                        rx.text("【必須】", color_scheme="red"),
                        spacing="2",
                    ),
                    rx.input(name="name", default_value=task_name),
                    rx.hstack(
                        rx.text("優先度"),
                        rx.text("【必須】", color_scheme="red"),
                        spacing="2",
                    ),
                    rx.select(["低", "中", "高"], default_value="高", name="priority"),
                    rx.hstack(
                        rx.text("カテゴリ"),
                        rx.text("【任意】", color_scheme="gray"),
                        spacing="2",
                    ),
                    rx.input(name="category"),
                    rx.hstack(
                        rx.text("締切日時"),
                        rx.text("【必須】", color_scheme="red"),
                        spacing="2",
                    ),
                    rx.input(name="deadline", type="datetime-local"),
                    rx.hstack(
                        rx.text("所要時間"),
                        rx.text("【必須】", color_scheme="red"),
                        spacing="2",
                    ),
                    rx.hstack(
                        rx.input(name="hour", default_value="1", width="8%"),
                        rx.text("時間"),
                        rx.input(name="minute", default_value="0", width="8%"),
                        rx.text("分"),
                    ),
                    rx.hstack(
                        rx.text("メモ"),
                        rx.text("【任意】", color_scheme="gray"),
                        spacing="2",
                    ),
                    rx.text_area(name="memo"),
                    direction="column",
                    spacing="3",
                ),
                rx.flex(
                    rx.dialog.close(
                        rx.button(
                            "キャンセル",
                            color_scheme="gray",
                            variant="soft",
                        ),
                    ),
                    rx.dialog.close(
                        rx.button("追加", type="submit"),
                    ),
                    spacing="3",
                    margin_top="16px",
                    justify="end",
                ),
                on_submit=TaskTableState.add_task_to_db,
            ),
        ),
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
