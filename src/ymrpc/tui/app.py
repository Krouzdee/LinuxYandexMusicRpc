from textual.app import App, ComposeResult
from textual.containers import Container, Horizontal, Vertical
from textual.widgets import Header, Footer, Static, Button
from textual.screen import Screen

from ymrpc.config import load_config
from ymrpc.auth import get_token


class SetupScreen(Screen):
    BINDINGS = [
        ("escape", "app.pop_screen", "Back"),
    ]

    def compose(self) -> ComposeResult:
        yield Header()

        with Container(id="setup-container"):
            yield Static(
                "Connect Yandex Music",
                id="setup-title",
                classes="section-title",
            )

            yield Static(
                "Connect your Yandex Music account to get started.",
                id="setup-description",
            )

            yield Static(
                "Press the button below to start authorization.",
                id="setup-status",
            )

            yield Static(
                "The authorization link will appear here.",
                id="setup-link",
            )

            yield Static(
                "Your code will appear here.",
                id="setup-code",
            )

            yield Static(
                "You have successfully connected your Yandex Music account.",
                id="setup-success",
            )

            yield Button(
                "Get authorization code",
                id="btn-auth",
                variant="primary",
            )

            yield Button(
                "Back",
                id="btn-back",
                variant="default",
            )

        yield Footer()

    def on_mount(self) -> None:
        self.query_one("#setup-success", Static).display = False
        self.query_one("#btn-back", Button).display = False

    def update_widget(self, selector: str, text: str) -> None:
        self.app.call_from_thread(
            lambda: self.query_one(selector, Static).update(text)
        )

    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "btn-auth":
            self.start_auth()
        elif event.button.id == "btn-back":
            self.app.pop_screen()

    def start_auth(self) -> None:
        auth_button = self.query_one("#btn-auth", Button)
        auth_button.disabled = True

        self.query_one("#setup-status", Static).update(
            "Starting authorization..."
        )

        def show_code(url: str, code: str) -> None:
            self.update_widget("#setup-link", f"Open: {url}")
            self.update_widget("#setup-code", f"Enter code: {code}")
            self.update_widget(
                "#setup-status",
                "Authorize LinuxYMRpc in your browser.",
            )

        def success() -> None:
            self.app.call_from_thread(self.show_success)

        def error(message: str) -> None:
            def update_error() -> None:
                self.query_one("#setup-status", Static).update(
                    f"Authorization failed: {message}"
                )
                self.query_one("#btn-auth", Button).disabled = False

            self.app.call_from_thread(update_error)

        get_token(show_code, success, error)

    def show_success(self) -> None:
        self.query_one("#setup-description", Static).display = False
        self.query_one("#setup-status", Static).display = False
        self.query_one("#setup-link", Static).display = False
        self.query_one("#setup-code", Static).display = False
        self.query_one("#btn-auth", Button).display = False

        self.query_one("#setup-title", Static).update(
            "Successfully authorized!"
        )
        self.query_one("#setup-success", Static).display = True
        self.query_one("#btn-back", Button).display = True


class ConfigScreen(Screen):
    BINDINGS = [
        ("escape", "app.pop_screen", "Back"),
    ]

    def compose(self) -> ComposeResult:
        yield Header()

        with Container(id="config-container"):
            yield Static("Settings", classes="section-title")
            yield Static("Coming soon", id="config-text")

            yield Button(
                "Back",
                id="btn-back",
                variant="error",
            )

        yield Footer()

    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "btn-back":
            self.app.pop_screen()


class YMRPCApp(App):
    TITLE = "LinuxYMRpc"
    SUB_TITLE = "Yandex Music Discord Rich Presence"

    BINDINGS = [
        ("q", "quit", "Quit"),
        ("c", "open_config", "Config"),
    ]

    CSS_PATH = "app.tcss"

    def compose(self) -> ComposeResult:
        yield Header()

        with Container(id="outer-frame"):
            with Vertical(id="main"):

                # Section 1: Header and status
                with Container(
                    id="header-section",
                    classes="section",
                ):
                    with Horizontal(id="header-row"):
                        yield Static("LinuxYMRpc", id="heading")
                        yield Static("Status", id="daemon-status")

                # Section 2: Now Playing
                with Container(classes="section"):
                    yield Static(
                        "Now Playing",
                        classes="section-title",
                    )
                    yield Static(
                        "Track Title — Artist Name",
                        id="now-playing",
                    )

                # Section 3: Configuration
                with Button(
                    id="config-btn",
                    classes="section config-card",
                ):
                    yield Static(
                        "Configuration",
                        classes="section-title",
                    )
                    yield Static(
                        "Manage service, startup and RPC display settings",
                        id="config-desc",
                    )

        yield Footer()

    def on_mount(self) -> None:
        load_config()

    def action_open_config(self) -> None:
        if isinstance(self.screen, (ConfigScreen, SetupScreen)):
            return

        config = load_config()
        token = config.get("yandex_token")

        if token and token.strip():
            self.push_screen(ConfigScreen())
        else:
            self.push_screen(SetupScreen())

    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "config-btn":
            self.action_open_config()


def main() -> None:
    YMRPCApp().run()


if __name__ == "__main__":
    main()
