
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

    async def create(self, name, email, phone, bio, about_me, github_url, linkedin_url, website_url, avatar_url, favicon_url):
        async with self.db.pool.connection() as conn:
            async with conn.cursor(row_factory=dict_row) as curr:
                await curr.execute("""
                    INSERT INTO basic_info (name, email, phone, bio, about_me, github_url, linkedin_url, website_url, avatar_url, favicon_url)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                    RETURNING *
                """, (name, email, phone, bio, about_me, github_url, linkedin_url, website_url, avatar_url, favicon_url))
                result = await curr.fetchone()
                await conn.commit()
                return result

    async def update(self, id:int, data:dict):
        async with self.db.pool.connection() as conn:
            async with conn.cursor(row_factory=dict_row) as curr:
                set_clause = ", ".join([f"{key} = %s" for key in data.keys()])
                values = list(data.values())
                values.append(id)
                await curr.execute(f"""
                    UPDATE basic_info
                    SET {set_clause}
                    WHERE id = %s
                    RETURNING *
                """, values)
                result = await curr.fetchone()
                await conn.commit()
                return result

    async def delete(self, id: int):
        async with self.db.pool.connection() as conn:
            async with conn.cursor(row_factory=dict_row) as curr:
                await curr.execute("""
                    DELETE FROM basic_info
                    WHERE id = %s
                    RETURNING *
                """, (id,))
                result = await curr.fetchone()
                await conn.commit()
                return result