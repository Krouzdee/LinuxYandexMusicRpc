import json
from pathlib import Path

CONFIG_DIR = Path.home() / ".config" / "LinuxYMRpc"
CONFIG_FILE = CONFIG_DIR / "config.json"

DEFAULT_CONFIG = {
    "yandex_token": "",
    "discord_client_id": "1269807014393942046",
    "show_cover": True,
}

def save_config(config: dict) -> None:
    CONFIG_DIR.mkdir(parents=True, exist_ok=True)

    with CONFIG_FILE.open("w", encoding="utf-8") as file:
        json.dump(config, file, indent=4, ensure_ascii=False)

def load_config() -> dict:
    CONFIG_DIR.mkdir(parents=True, exist_ok=True)

    if not CONFIG_FILE.exists():
        save_config(DEFAULT_CONFIG.copy())

    with CONFIG_FILE.open("r", encoding="utf-8") as file:
        return json.load(file)