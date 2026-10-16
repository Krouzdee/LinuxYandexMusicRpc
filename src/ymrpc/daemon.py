from yandex_music.ynison.client import YnisonClient
from pypresence import Presence
from pypresence.types import ActivityType

from ymrpc.config import load_config

def main() -> None:
    config = load_config()
    token = config["yandex_token"]
    discord_client_id = config["discord_client_id"]

    if not token:
        print("Yandex Token not found")
        return

    rpc = Presence(discord_client_id)
    client = YnisonClient(token)

    try:
        rpc.connect()
        print("RPC conected")

        @client.on_state
        def on_state(state):
            status = state.player_state.status
            track = client.current_playable
            print(f"Now played: {track}")

            if status.paused or track is None:
                rpc.clear()
                return

            artists = ", ".join(artist.name for artist in track.artists) if track.artists else "Unknowm artist"

            rpc.update(
                activity_type=ActivityType.LISTENING,
                details=track.title,
                state=f"by {artists}",
            )

    
        client.connect()
    except KeyboardInterrupt:
            pass
    finally:
        client.disconnect()
        rpc.clear()
        rpc.close()

if __name__ == "__main__":
    main()