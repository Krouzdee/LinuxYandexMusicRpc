from textual.app import App, ComposeResult
from textual.containers import Container, Horizontal, Vertical
from textual.widgets import Header, Footer, Static


class YMRPCApp(App):
    TITLE = "LinuxYMRpc"
    SUB_TITLE = "Yandex Music Discord Rich Presence"

    BINDINGS = [
        ("q", "quit", "Quit"),
        ("c", "open_config", "Configuration"),
    ]

    CSS_PATH = "app.tcss"

    def compose(self) -> ComposeResult:
        yield Header()

        with Container(id="outer-frame"):
            with Vertical(id="main"):
                # Section 1
                with Container(id="header-section", classes="section"):
                    with Horizontal(id="header-row"):
                        yield Static("LinuxYMRpc", id="heading")
                        yield Static("Status", id="daemon-status")

                # Section 2
                with Container(classes="section"):
                    yield Static("Now Playing", classes="section-title")
                    yield Static(
                        "Track Title — Artist Name",
                        id="now-playing",
                    )

                # Section 3
                with Container(classes="section"):
                    yield Static("Configuration", classes="section-title")
                    yield Static(
                        "Manage service, startup and RPC display settings",
                        id="config-desc",
                    )

        

        yield Footer()



    def action_open_config(self) -> None:
        # We'll implement the configuration screen next.
        pass


if __name__ == "__main__":
    YMRPCApp().run()