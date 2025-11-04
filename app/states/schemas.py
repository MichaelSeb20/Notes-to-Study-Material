import reflex as rx
from typing import TypedDict


class Broadcast(TypedDict):
    id: str
    title: str
    content: str
    date: str


class Flashcard(TypedDict):
    id: str
    question: str
    answer: str


class Note(TypedDict):
    id: str
    title: str
    content: str
    date: str
    file_type: str
    flashcards: list[Flashcard]
    summary: str | None
    broadcasts: list[Broadcast]