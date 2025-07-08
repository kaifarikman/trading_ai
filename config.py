import os
from dotenv import load_dotenv
load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
ADMIN_PEER_ID = os.getenv("ADMIN_PEER_ID")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

user = os.getenv("user")
password = os.getenv("password")
host = os.getenv("host")
port = os.getenv("port")
database = os.getenv("database")


DB_CONNECTION_URL = f"postgresql+asyncpg://{user}:{password}@{host}:{port}/{database}"
