
from concurrent.futures import ThreadPoolExecutor
from typing import Callable

from yandex_music import Client

from ymrpc.config import load_config, save_config


_executor = ThreadPoolExecutor(max_workers=1)


def get_token(
    on_code: Callable[[str, str], None],
    on_success: Callable[[], None],
    on_error: Callable[[str], None],
) -> None:
    """Run device authorization in a background thread."""

    def on_device_code(code) -> None:
        on_code(code.verification_url, code.user_code)

    def worker() -> None:
        try:
            client = Client()
            token = client.device_auth(on_code=on_device_code)

            config = load_config()
            config["yandex_token"] = token.access_token
            save_config(config)

            on_success()
        except Exception as error:
            on_error(str(error))

    _executor.submit(worker)
