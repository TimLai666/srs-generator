"""Welcome to Reflex! This file outlines the steps to create a basic app."""

from srs_generator.srs_map import srs_map
from srs_generator.llm import generate_srs
import reflex as rx
import ssl
import os
os.environ['CURL_CA_BUNDLE'] = ''
os.environ['PYTHONHTTPSVERIFY'] = '0'
ssl._create_default_https_context = ssl._create_unverified_context


class State(rx.State):
    """The app state."""

    proj_name: str = ""
    proj_requirements: str = ""
    srs_result: str = ""

    @rx.event
    def generate_srs(self):
        self.srs_result = generate_srs(
            srs_map, self.proj_name, self.proj_requirements)


def index() -> rx.Component:
    # Welcome Page (Index)
    return rx.center(
        rx.card(
            rx.vstack(
                rx.heading("SRS 產生器", size="4", mb="4"),
                rx.input(
                    placeholder="輸入專案名稱",
                    value=State.proj_name,
                    on_change=State.set_proj_name,
                    width="100%",
                    mb="3"
                ),
                rx.text_area(
                    placeholder="輸入專案需求",
                    value=State.proj_requirements,
                    on_change=State.set_proj_requirements,
                    width="100%",
                    rows="6",
                    mb="3"
                ),
                rx.button(
                    "生成",
                    color_scheme="blue",
                    width="100%",
                    on_click=State.generate_srs
                ),
                rx.text(State.srs_result, mt="4",
                        width="100%", white_space="pre-wrap"),
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
