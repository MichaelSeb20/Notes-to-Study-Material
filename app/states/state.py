import reflex as rx
import datetime
import uuid
from .schemas import Note


class State(rx.State):
    """The base state for the app."""

    notes: list[Note] = []
    upload_status: str = ""
    selected_note_id: str | None = None
    show_preview: bool = False
    is_generating: bool = False
    generated_summary: str = ""

    @rx.event
    async def handle_upload(self, files: list[rx.UploadFile]):
        self.upload_status = "Uploading..."
        yield
        for file in files:
            upload_data = await file.read()
            file_path = rx.get_upload_dir() / file.name
            with file_path.open("wb") as f:
                f.write(upload_data)
            new_note: Note = {
                "id": str(uuid.uuid4()),
                "title": file.name,
                "content": upload_data.decode("utf-8", errors="ignore"),
                "date": datetime.datetime.now().strftime("%Y-%m-%d"),
                "file_type": file.content_type,
                "flashcards": [],
                "summary": None,
                "broadcasts": [],
            }
            self.notes.append(new_note)
        self.upload_status = "Upload complete!"
        yield rx.clear_selected_files("upload_area")

    @rx.event
    def select_note(self, note_id: str):
        self.selected_note_id = note_id
        self.show_preview = True

    @rx.event
    def close_preview(self):
        self.selected_note_id = None
        self.show_preview = False

    @rx.event
    def delete_note(self, note_id: str):
        self.notes = [note for note in self.notes if note["id"] != note_id]

    @rx.event
    def generate_summary(self):
        self.is_generating = True
        yield
        note = self.selected_note
        if not note:
            self.is_generating = False
            return
        self.generated_summary = f"This is a summary for '{note['title']}'. It covers the main points and key takeaways from the document. The content includes..."
        for i, n in enumerate(self.notes):
            if n["id"] == self.selected_note_id:
                pass
        self.is_generating = False
        self.show_preview = False
        yield rx.redirect("/summary")

    @rx.event
    def generate_flashcards(self):
        self.is_generating = True
        yield
        note = self.selected_note
        if not note:
            self.is_generating = False
            return
        new_flashcards = [
            {
                "id": str(uuid.uuid4()),
                "question": "What is the capital of France?",
                "answer": "Paris",
            },
            {
                "id": str(uuid.uuid4()),
                "question": "Who wrote 'To Kill a Mockingbird'?",
                "answer": "Harper Lee",
            },
        ]
        for i, n in enumerate(self.notes):
            if n["id"] == self.selected_note_id:
                self.notes[i]["flashcards"] = new_flashcards
                break
        self.is_generating = False
        self.show_preview = False
        yield rx.redirect("/flashcards")

    @rx.event
    def generate_broadcast(self):
        self.is_generating = True
        yield
        note = self.selected_note
        if not note:
            self.is_generating = False
            return
        new_broadcast = {
            "id": str(uuid.uuid4()),
            "title": f"Broadcast for {note['title']}",
            "content": f"This is a broadcast generated from the note: {note['title']}. Here's the content:\n\n{note['content']}",
            "date": datetime.datetime.now().strftime("%Y-%m-%d"),
        }
        for i, n in enumerate(self.notes):
            if n["id"] == self.selected_note_id:
                if (
                    "broadcasts" not in self.notes[i]
                    or self.notes[i]["broadcasts"] is None
                ):
                    self.notes[i]["broadcasts"] = []
                self.notes[i]["broadcasts"].append(new_broadcast)
                break
        self.is_generating = False
        self.show_preview = False
        yield rx.redirect("/broadcasts")

    @rx.var
    def selected_note(self) -> Note | None:
        if self.selected_note_id is None:
            return None
        for note in self.notes:
            if note["id"] == self.selected_note_id:
                return note
        return None