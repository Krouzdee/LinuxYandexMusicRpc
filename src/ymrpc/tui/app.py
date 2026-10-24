from textual.app import App, ComposeResult
from textual.containers import Container, Horizontal, Vertical
from textual.widgets import Header, Footer, Static, Button
from textual.screen import Screen


class ConfigScreen(Screen):
    BINDINGS = [
        ("escape", "app.pop_screen", "Back")
    ]

    def compose(self) -> ComposeResult:
        yield Header()
        with Container(id="config-container"):
            yield Static("Settings", classes="section-title")
            yield Static("Coming soon", id="config-text")

            yield Button("Back", id="btn-back", variant="error")

        yield Footer()

class YMRPCApp(App):
    TITLE = "LinuxYMRpc"
    SUB_TITLE = "Yandex Music Discord Rich Presence"

    BINDINGS = [
        ("q", "quit", "Quit"),
        ("c", "open_config", "Config")
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
                with Button(id="config-btn", classes="section config-card"):
                    yield Static("Configuration", classes="section-title")
                    yield Static(
                        "Manage service, startup and RPC display settings",
                        id="config-desc",
                    )

        
        yield Footer()



    def action_open_config(self) -> None:
        self.push_screen(ConfigScreen())

    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "config-btn":
            self.action_open_config()
        elif event.button.id == "btn-back":
            self.app.pop_screen()


if __name__ == "__main__":
    YMRPCApp().run()