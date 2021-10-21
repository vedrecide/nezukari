import os
import dotenv

from typing import Final

dotenv.load_dotenv()


class Config:
    token: Final[str] = os.getenv("BOT_TOKEN")
    host: Final[str] = os.getenv("LAVALINK_HOST")
    password: Final[str] = os.getenv("LAVALINK_PASSWORD")
