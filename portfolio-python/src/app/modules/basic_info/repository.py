
from app.config.database import DatabaseManager
from psycopg.rows import dict_row


class BasicInfoRepository:

    def __init__(self, db: DatabaseManager):
        self.db = db

    async def init(self) -> None:
        async with self.db.pool.connection() as conn:
            async with conn.cursor() as cur:
                await cur.execute("""
                    CREATE TABLE IF NOT EXISTS basic_info (
                        id SERIAL PRIMARY KEY,
                        name VARCHAR(255) NOT NULL,
                        email VARCHAR(255) NOT NULL,
                        phone BIGINT NOT NULL,
                        bio TEXT NOT NULL,
                        about_me TEXT NOT NULL,
                        github_url VARCHAR(255) NOT NULL,
                        linkedin_url VARCHAR(255) NOT NULL,
                        website_url VARCHAR(255) NOT NULL,
                        avatar_url VARCHAR(255) NOT NULL,
                        favicon_url VARCHAR(255) NOT NULL
                    )
                """)
                await conn.commit()

    async def get(self):
        async with self.db.pool.connection() as conn:
            async with conn.cursor(row_factory=dict_row) as cur:
                await cur.execute("SELECT * FROM basic_info")
                result = await cur.fetchone()
                return result