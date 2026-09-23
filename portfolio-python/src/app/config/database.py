import os
from psycopg_pool import AsyncConnectionPool
from dotenv import load_dotenv

load_dotenv(dotenv_path=".env.local")

class DatabaseManager:
    def __init__(self):
        self.db_host = os.getenv("DB_HOST")
        self.db_port = os.getenv("DB_PORT")
        self.db_user = os.getenv("DB_USER")
        self.db_password = os.getenv("DB_PASSWORD")
        self.db_name = os.getenv("DB_NAME")
        self.conninfo = f"postgresql://{self.db_user}:{self.db_password}@{self.db_host}:{self.db_port}/{self.db_name}"

        self.pool: AsyncConnectionPool = None

    async def connect(self) -> None:
        """Establish a connection pool and initialize the database schema."""
        self.pool = AsyncConnectionPool(conninfo=self.conninfo, open=False)
        await self.pool.open()

    async def disconnect(self) -> None:
        """Close the connection pool."""
        if self.pool:
            await self.pool.close()

# Singleton instance of the DatabaseManager class.
db_manager = DatabaseManager()