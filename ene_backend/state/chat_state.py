from ..db_model import Task
from ..utils.gpt_utils import call_gpt, create_Client, create_compliment_prompt
from .task_state import TaskTableState


class ChatState(TaskTableState):
    question: str = ""
    response: str = ""
    chat_history: list[tuple[str, str]] = []

    def get_response(self, task: Task) -> str:
        client = create_Client()
        duration = int(task["hour"]) * 60 + int(task["minute"])
        prompt = create_compliment_prompt(username=self.name, taskname=task["name"], duration=duration, fav=self.fav)
        return call_gpt(client, prompt)

    def reflesh(self) -> None:
        self.chat_history = []

    def answer(self, task: Task) -> None:
        self.question = f"「{task["name"]}」が終わったよ！褒めて！"
        try:
            self.complete_task(task)
        except:
            return
        self.response = self.get_response(task)
        self.chat_history.append((self.question, self.response))
