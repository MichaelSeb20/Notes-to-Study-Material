import reflex as rx
from app.states.state import State
from app.components.sidebar import sidebar
from app.states.schemas import Note, Flashcard


def note_preview_modal() -> rx.Component:
    return rx.radix.primitives.dialog.root(
        rx.radix.primitives.dialog.portal(
            rx.radix.primitives.dialog.overlay(
                class_name="fixed inset-0 bg-black/30 backdrop-blur-sm z-40"
            ),
            rx.radix.primitives.dialog.content(
                rx.radix.primitives.dialog.title(
                    rx.cond(State.selected_note, State.selected_note["title"], ""),
                    class_name="text-xl font-semibold text-gray-900",
                ),
                rx.el.div(
                    rx.markdown(
                        rx.cond(
                            State.selected_note,
                            State.selected_note["content"],
                            "No content available.",
                        ),
                        class_name="prose max-w-full",
                    ),
                    class_name="mt-4 max-h-[70vh] overflow-y-auto p-1",
                ),
                rx.el.div(
                    rx.el.div(
                        rx.radix.primitives.dialog.close(
                            rx.el.button(
                                "Close",
                                class_name="mt-4 px-4 py-2 bg-gray-200 text-gray-800 rounded-md hover:bg-gray-300",
                            )
                        ),
                        rx.el.button(
                            rx.cond(
                                State.is_generating,
                                rx.el.div(
                                    rx.spinner(class_name="mr-2"),
                                    "Generating...",
                                    class_name="flex items-center",
                                ),
                                "Generate Summary",
                            ),
                            on_click=State.generate_summary,
                            disabled=State.is_generating,
                            class_name="mt-4 ml-2 px-4 py-2 bg-green-600 text-white rounded-md hover:bg-green-700 disabled:bg-green-300 transition-colors",
                        ),
                        rx.el.button(
                            rx.cond(
                                State.is_generating,
                                rx.el.div(
                                    rx.spinner(class_name="mr-2"),
                                    "Generating...",
                                    class_name="flex items-center",
                                ),
                                "Generate Broadcast",
                            ),
                            on_click=State.generate_broadcast,
                            disabled=State.is_generating,
                            class_name="mt-4 ml-2 px-4 py-2 bg-purple-600 text-white rounded-md hover:bg-purple-700 disabled:bg-purple-300 transition-colors",
                        ),
                        rx.el.button(
                            rx.cond(
                                State.is_generating,
                                rx.el.div(
                                    rx.spinner(class_name="mr-2"),
                                    "Generating...",
                                    class_name="flex items-center",
                                ),
                                "Generate Flashcards",
                            ),
                            on_click=State.generate_flashcards,
                            disabled=State.is_generating,
                            class_name="mt-4 ml-2 px-4 py-2 bg-blue-600 text-white rounded-md hover:bg-blue-700 disabled:bg-blue-300 transition-colors",
                        ),
                        class_name="flex justify-end pt-4 items-center",
                    ),
                    class_name="flex justify-between pt-4",
                ),
                class_name="fixed top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 bg-white rounded-xl shadow-2xl p-6 w-full max-w-2xl z-50",
            ),
        ),
        open=State.show_preview,
    )


def note_card(note: Note) -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.icon("file-text", class_name="w-8 h-8 text-gray-400"),
            class_name="p-4 bg-gray-100 rounded-t-lg",
        ),
        rx.el.div(
            rx.el.h3(note["title"], class_name="font-semibold truncate"),
            rx.el.p(f"Date: {note['date']}", class_name="text-sm text-gray-500"),
            class_name="p-4",
        ),
        on_click=lambda: State.select_note(note["id"]),
        class_name="bg-white border border-gray-200 rounded-lg shadow-sm hover:shadow-md transition-shadow cursor-pointer",
    )


def upload_component() -> rx.Component:
    return rx.el.div(
        rx.upload.root(
            rx.el.div(
                rx.icon("cloud-upload", class_name="w-10 h-10 text-gray-400"),
                rx.el.p("Drag & drop files here, or click to select files"),
                class_name="flex flex-col items-center justify-center p-8 border-2 border-dashed border-gray-300 rounded-lg bg-gray-50 hover:bg-gray-100 transition-colors",
            ),
            id="upload_area",
            multiple=True,
            accept={
                "text/plain": [".txt"],
                "application/pdf": [".pdf"],
                "application/vnd.openxmlformats-officedocument.wordprocessingml.document": [
                    ".docx"
                ],
                "text/markdown": [".md"],
            },
            class_name="w-full mb-4",
        ),
        rx.el.div(
            rx.foreach(
                rx.selected_files("upload_area"),
                lambda file: rx.el.div(
                    rx.el.p(file, class_name="truncate"),
                    class_name="text-sm text-gray-700 bg-gray-100 rounded-md px-2 py-1",
                ),
            ),
            class_name="flex flex-wrap gap-2 mb-4",
        ),
        rx.el.button(
            "Upload",
            on_click=State.handle_upload(rx.upload_files(upload_id="upload_area")),
            class_name="px-6 py-2 bg-blue-600 text-white rounded-md hover:bg-blue-700 transition-colors",
        ),
        rx.el.p(State.upload_status, class_name="mt-2 text-sm text-gray-600"),
    )


def index() -> rx.Component:
    return rx.el.div(
        sidebar(),
        rx.el.main(
            rx.el.h1("My Notes", class_name="text-2xl font-bold text-gray-900 mb-6"),
            upload_component(),
            rx.el.hr(class_name="my-6"),
            rx.el.h2("Library", class_name="text-xl font-semibold text-gray-800 mb-4"),
            rx.el.div(
                rx.foreach(State.notes, note_card),
                class_name="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-4",
            ),
            note_preview_modal(),
            class_name="flex-1 p-6",
        ),
        class_name="flex min-h-screen w-full bg-white font-['Inter']",
    )


def flashcard_component(flashcard: Flashcard, index: int) -> rx.Component:
    return rx.el.div(
        rx.el.div(f"Q{index + 1}: {flashcard['question']}", class_name="font-semibold"),
        rx.el.p(f"A: {flashcard['answer']}", class_name="text-gray-600 mt-1"),
        class_name="bg-white p-4 border border-gray-200 rounded-lg shadow-sm",
    )


def flashcards_page() -> rx.Component:
    return rx.el.div(
        sidebar(),
        rx.el.main(
            rx.el.h1(
                "Flashcards for ",
                rx.el.span(
                    rx.cond(State.selected_note, State.selected_note["title"], ""),
                    class_name="font-bold",
                ),
                class_name="text-2xl text-gray-900 mb-6",
            ),
            rx.cond(
                State.selected_note,
                rx.el.div(
                    rx.foreach(State.selected_note["flashcards"], flashcard_component),
                    class_name="grid grid-cols-1 md:grid-cols-2 gap-4",
                ),
                rx.el.div(
                    rx.el.p(
                        "No note selected or no flashcards generated. Go back to the dashboard to select a note."
                    ),
                    rx.el.a(
                        "Go to Dashboard",
                        href="/",
                        class_name="mt-4 inline-block px-4 py-2 bg-blue-600 text-white rounded-md",
                    ),
                    class_name="text-center p-8",
                ),
            ),
            class_name="flex-1 p-6",
        ),
        class_name="flex min-h-screen w-full bg-white font-['Inter']",
    )


app = rx.App(
    theme=rx.theme(appearance="light"),
    head_components=[
        rx.el.link(rel="preconnect", href="https://fonts.googleapis.com"),
        rx.el.link(rel="preconnect", href="https://fonts.gstatic.com", cross_origin=""),
        rx.el.link(
            href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600&display=swap",
            rel="stylesheet",
        ),
    ],
)


def summary_page() -> rx.Component:
    return rx.el.div(
        sidebar(),
        rx.el.main(
            rx.el.h1(
                "Generated Summary for ",
                rx.el.span(
                    rx.cond(State.selected_note, State.selected_note["title"], ""),
                    class_name="font-bold",
                ),
                class_name="text-2xl text-gray-900 mb-6",
            ),
            rx.cond(
                State.generated_summary,
                rx.el.div(
                    rx.markdown(State.generated_summary, class_name="prose max-w-full"),
                    class_name="p-6 bg-white border border-gray-200 rounded-lg shadow-sm",
                ),
                rx.el.div(
                    rx.el.p(
                        "No summary available. Go back to the dashboard to generate one."
                    ),
                    rx.el.a(
                        "Go to Dashboard",
                        href="/",
                        class_name="mt-4 inline-block px-4 py-2 bg-blue-600 text-white rounded-md",
                    ),
                    class_name="text-center p-8",
                ),
            ),
            class_name="flex-1 p-6",
        ),
        class_name="flex min-h-screen w-full bg-white font-['Inter']",
    )


def broadcast_card(broadcast: dict) -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.el.h3(broadcast["title"], class_name="font-semibold text-gray-800"),
            rx.el.p(f"Date: {broadcast['date']}", class_name="text-sm text-gray-500"),
            class_name="flex-1",
        ),
        rx.el.button(
            rx.icon(tag="download", class_name="w-4 h-4 mr-2"),
            "Download",
            on_click=rx.download(
                data=broadcast["content"], filename=f"{broadcast['title']}.txt"
            ),
            class_name="px-3 py-1 bg-gray-200 text-gray-700 text-sm rounded-md hover:bg-gray-300 transition-colors flex items-center",
        ),
        class_name="bg-white p-4 border border-gray-200 rounded-lg shadow-sm flex items-center justify-between",
    )


def broadcasts_page() -> rx.Component:
    return rx.el.div(
        sidebar(),
        rx.el.main(
            rx.el.h1(
                "Broadcasts for ",
                rx.el.span(
                    rx.cond(State.selected_note, State.selected_note["title"], ""),
                    class_name="font-bold",
                ),
                class_name="text-2xl text-gray-900 mb-6",
            ),
            rx.cond(
                State.selected_note,
                rx.el.div(
                    rx.foreach(State.selected_note["broadcasts"], broadcast_card),
                    class_name="grid grid-cols-1 gap-4",
                ),
                rx.el.div(
                    rx.el.p(
                        "No note selected or no broadcasts generated. Go back to the dashboard to select a note."
                    ),
                    rx.el.a(
                        "Go to Dashboard",
                        href="/",
                        class_name="mt-4 inline-block px-4 py-2 bg-blue-600 text-white rounded-md",
                    ),
                    class_name="text-center p-8",
                ),
            ),
            class_name="flex-1 p-6",
        ),
        class_name="flex min-h-screen w-full bg-white font-['Inter']",
    )


from app.states.chat_state import ChatState, Message


def message_bubble(message: Message) -> rx.Component:
    is_user = message["role"] == "user"
    return rx.el.div(
        rx.el.div(
            rx.el.div(
                rx.markdown(message["content"], class_name="prose"),
                class_name=rx.cond(
                    is_user, "bg-blue-500 text-white", "bg-gray-200 text-gray-800"
                ),
                style={
                    "padding": "10px 15px",
                    "border_radius": "20px",
                    "max_width": "70%",
                },
            ),
            class_name="flex",
            style={"justify_content": rx.cond(is_user, "flex-end", "flex-start")},
        ),
        class_name="w-full p-2",
    )


def chat_page() -> rx.Component:
    return rx.el.div(
        sidebar(),
        rx.el.main(
            rx.el.div(
                rx.el.div(
                    rx.foreach(ChatState.messages, message_bubble),
                    class_name="flex-grow overflow-y-auto p-4 space-y-4",
                ),
                rx.el.div(
                    rx.el.form(
                        rx.el.input(
                            placeholder="Ask me anything...",
                            name="chat_input",
                            class_name="flex-grow p-3 border rounded-l-lg focus:outline-none focus:ring-2 focus:ring-blue-500",
                        ),
                        rx.el.button(
                            rx.icon("send", class_name="w-5 h-5"),
                            type="submit",
                            disabled=ChatState.is_processing,
                            class_name="p-3 bg-blue-600 text-white rounded-r-lg hover:bg-blue-700 disabled:bg-blue-300 flex items-center justify-center",
                        ),
                        on_submit=ChatState.handle_submit,
                        reset_on_submit=True,
                        class_name="flex w-full",
                    ),
                    class_name="p-4 bg-white border-t",
                ),
                class_name="flex flex-col h-full",
            ),
            class_name="flex-1 flex flex-col h-[calc(100vh)] bg-gray-50",
        ),
        class_name="flex min-h-screen w-full bg-white font-['Inter']",
    )


app.add_page(index)
app.add_page(flashcards_page, route="/flashcards")
app.add_page(summary_page, route="/summary")
app.add_page(broadcasts_page, route="/broadcasts")
app.add_page(chat_page, route="/chat")