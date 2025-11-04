import reflex as rx


def nav_item(icon: str, text: str, href: str, selected: bool) -> rx.Component:
    return rx.el.a(
        rx.icon(icon, class_name="h-5 w-5"),
        rx.el.span(text, class_name="font-medium"),
        href=href,
        class_name=rx.cond(
            selected,
            "flex items-center gap-3 rounded-lg bg-gray-100 px-3 py-2 text-gray-900 transition-all hover:text-gray-900",
            "flex items-center gap-3 rounded-lg px-3 py-2 text-gray-500 transition-all hover:text-gray-900",
        ),
    )


def sidebar() -> rx.Component:
    return rx.el.aside(
        rx.el.div(
            rx.el.a(
                rx.icon("book-open-text", class_name="h-6 w-6"),
                rx.el.span("Flashcard AI", class_name="text-lg font-semibold"),
                href="#",
                class_name="flex items-center gap-2 p-4 border-b",
            ),
            rx.el.nav(
                nav_item("home", "Dashboard", "/", True),
                nav_item("message-circle", "AI Chat", "/chat", False),
                nav_item("book-marked", "My Notes", "#", False),
                nav_item("copy", "Flashcards", "/flashcards", False),
                nav_item("file-text", "Summaries", "/summary", False),
                nav_item("radio-tower", "Broadcasts", "/broadcasts", False),
                nav_item("settings", "Settings", "#", False),
                class_name="flex flex-col gap-1 p-4 text-sm font-medium",
            ),
            class_name="flex flex-col h-full",
        ),
        class_name="hidden md:flex flex-col w-64 border-r bg-gray-100/40",
    )