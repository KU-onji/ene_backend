import reflex as rx


class ChatState(rx.State):
    question: str = "Hello!"
    response: str = "Hello, world!"
    chat_history: list[tuple[str, str]] = [
        ("Hello", "Hi"),
        ("How are you?", "I'm fine."),
    ]

    def answer(self):
        self.chat_history.append((self.question, self.response))
