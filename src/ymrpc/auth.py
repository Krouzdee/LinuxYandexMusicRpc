from yandex_music import Client

from ymrpc.config import load_config, save_config

def on_code(code):
    print(f"Open page: {code.verification_url}")
    print(f"Enter code: {code.user_code}")


def get_token():
    client = Client()
    token = client.device_auth(on_code=on_code)

    config = load_config()
    config["yandex_token"] = token.access_token
    save_config(config)

    print("Config saved")

if __name__ == "__main__":
    get_token()