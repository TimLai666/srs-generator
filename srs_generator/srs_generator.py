"""Welcome to Reflex! This file outlines the steps to create a basic app."""

from srs_generator.srs_map import srs_map
from srs_generator.llm import generate_srs
from srs_generator.render_srs import render_srs_from_llm_response
import reflex as rx
import urllib.parse


class State(rx.State):
    """The app state."""

    proj_name: str = ""
    proj_requirements: str = ""
    srs_result: str = ""
    loading: bool = False

    @rx.event
    async def generate_srs(self):
        self.loading = True
        import ssl
        import os
        os.environ['CURL_CA_BUNDLE'] = ''
        os.environ['PYTHONHTTPSVERIFY'] = '0'
        ssl._create_default_https_context = ssl._create_unverified_context
        self.srs_result = render_srs_from_llm_response(self.proj_name, generate_srs(
            srs_map, self.proj_name, self.proj_requirements))
        self.loading = False


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
                rx.cond(
                    State.loading,
                    rx.spinner(width="100%", thickness="4px",
                               color="blue.500", size="3", speed="0.65s", mt="1"),
                    rx.button(
                        "生成",
                        color_scheme="blue",
                        width="100%",
                        on_click=State.generate_srs,
                        is_disabled=State.loading
                    )
                ),
                rx.text(State.srs_result, mt="4",
                        width="100%", white_space="pre-wrap"),
                rx.cond(
                    State.srs_result != "",
                    rx.link(
                        rx.button(
                            "下載 SRS 結果",
                            color_scheme="teal",
                            width="100%",
                            mt="2"
                        ),
                        download=rx.cond(
                            State.proj_name != "", State.proj_name + ".txt", "SRS.txt"),
                        href=rx.cond(
                            State.srs_result != "",
                            "data:text/plain;charset=utf-8," +
                            urllib.parse.quote(str(State.srs_result)),
                            ""
                        )
                    ),
                    None
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
