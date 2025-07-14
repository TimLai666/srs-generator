"""Welcome to Reflex! This file outlines the steps to create a basic app."""

import reflex as rx


class State(rx.State):
    """The app state."""


def index() -> rx.Component:
    # Welcome Page (Index)
    return rx.center(
        rx.card(
            rx.vstack(
                rx.heading("SRS 產生器", size="4", mb="4"),
                rx.form(
                    rx.vstack(
                        rx.input(
                            placeholder="輸入專案名稱",
                            name="proj_name",
                            width="100%",
                            mb="3"
                        ),
                        rx.text_area(
                            name="proj_requirements",
                            placeholder="輸入專案需求",
                            width="100%",
                            rows="6",
                            mb="3"
                        ),
                        rx.button("生成", color_scheme="blue", width="100%")
                    ),
                    width="100%"
                ),
                spacing="4",
                width="100%"
            ),
            width="400px",
            p="8",
            shadow="lg"
        ),
        min_h="100vh",
        bg="gray.50"
    )


app = rx.App()
app.add_page(index)
