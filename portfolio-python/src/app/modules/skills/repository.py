
from psycopg.rows import dict_row

from app.config.database import DatabaseManager


class SkillRepository:
    def __init__(self, db: DatabaseManager):
        self.db = db

    async def init(self):
        async with self.db.pool.connection() as conn:
            async with conn.cursor() as cur:
                await cur.execute("""
                    CREATE TABLE IF NOT EXISTS skills (
                        id SERIAL PRIMARY KEY,
                        name VARCHAR(255) NOT NULL,
                        category VARCHAR(255) NOT NULL,
                        proficiency_level VARCHAR(255) NOT NULL,
                        years_of_experience INT NOT NULL,
                        icon_name VARCHAR(255) NOT NULL,
                        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                        updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                    )
                """)
                await conn.commit()
    
    
    async def get_all_skills(self):
        async with self.db.pool.connection() as conn:
            async with conn.cursor(row_factory=dict_row) as cur:
                await cur.execute("SELECT * FROM skills")
                result = await cur.fetchall()
                return result


    async def create (self, name, category, proficiency_level, years_of_experience, icon_name):
        async with self.db.pool.connection() as conn:
            async with conn.cursor(row_factory=dict_row) as cur:
                await cur.execute("""
                    INSERT INTO skills (name, category, proficiency_level, years_of_experience, icon_name)
                    VALUES (%s, %s, %s, %s, %s)
                    RETURNING *"""
                    , (name, category, proficiency_level, years_of_experience, icon_name)
                    )
                result = await cur.fetchone()
                await conn.commit()
                return result

    async def update (self, id, data: dict):
        async with self.db.pool.connection() as conn:
            async with conn.cursor(row_factory=dict_row) as cur:
                set_clause = ", ".join(f"{key} = %s" for key in data.keys())
                values = list(data.values())
                values.append(id)
                await cur.execute(f"""
                    UPDATE skills
                    SET {set_clause},
                        updated_at = CURRENT_TIMESTAMP
                    WHERE id = %s
                    RETURNING *"""
                    , values
                    )
                result = await cur.fetchone()
                await conn.commit()
                return result