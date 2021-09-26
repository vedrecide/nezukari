import os
import dotenv

dotenv.load_dotenv()

class Config:
    token = os.getenv("BOT_TOKEN")
    host = os.getenv("LAVALINK_HOST")
    password = os.getenv("LAVALINK_PASSWORD")
