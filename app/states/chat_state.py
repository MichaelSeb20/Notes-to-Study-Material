import reflex as rx
from typing import TypedDict
import asyncio


class Message(TypedDict):
    role: str
    content: str


class ChatState(rx.State):
    messages: list[Message] = []
    current_input: str = ""
    is_processing: bool = False

    @rx.event
    async def handle_submit(self, form_data: dict):
        user_input = form_data.get("chat_input", "").strip()
        if not user_input:
            return
        self.is_processing = True
        user_message: Message = {"role": "user", "content": user_input}
        self.messages.append(user_message)
        self.current_input = ""
        yield
        await asyncio.sleep(1)
        ai_response: Message = {
            "role": "assistant",
            "content": f"This is a simulated AI response to: '{user_message['content']}'",
        }
        self.messages.append(ai_response)
        self.is_processing = False
        yield