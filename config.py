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


def get_docker_link(name):
    return f'''sudo docker run -d --name {name} -e POSTGRES_PASSWORD={password} -e POSTGRES_USER={user} -e POSTGRES_DB={database} -p 5432:5432 postgres'''



