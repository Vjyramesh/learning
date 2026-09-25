

from psycopg.rows import dict_row


class CertificationRepository:
    def __init__(self, db):
        self.db = db

    async def init(self):
        async with self.db.pool.connection() as conn:
            async with conn.cursor() as cur:
                await cur.execute("""
                    CREATE TABLE IF NOT EXISTS certifications (
                        id SERIAL PRIMARY KEY,
                        name VARCHAR(255) NOT NULL,
                        issue_date VARCHAR(255) NOT NULL,
                        expiration_date VARCHAR(255),
                        credential_id VARCHAR(255),
                        credential_url VARCHAR(255),
                        issuing_organization VARCHAR(255) NOT NULL
                    )
                """)
    async def get_all(self):
        async with self.db.pool.connection() as conn:
            async with conn.cursor(row_factory=dict_row) as cur:
                await cur.execute("SELECT * FROM certifications")
                result = await cur.fetchall()
                return result

    async def create_certification(self, name, issuing_organization, issue_date, expiration_date=None, credential_id=None, credential_url=None):
        async with self.db.pool.connection() as conn:
            async with conn.cursor(row_factory=dict_row) as cur:
                await cur.execute("""
                    INSERT INTO certifications (name, issuing_organization, issue_date, expiration_date, credential_id, credential_url)
                    VALUES (%s, %s, %s, %s, %s, %s)
                    RETURNING *
                """, (name, issuing_organization, issue_date, expiration_date, credential_id, credential_url))
                result = await cur.fetchone()
                await conn.commit()
                return result

    async def update_certification(self, id, data):
        async with self.db.pool.connection() as conn:
            async with conn.cursor(row_factory=dict_row) as cur:
                set_clause = ", ".join(f"{key} = %s" for key in data.keys())
                values = list(data.values())
                values.append(id)
                await cur.execute(f"""
                    UPDATE certifications
                    SET {set_clause}
                    WHERE id = %s
                    RETURNING *
                """, (*values,))
                result = await cur.fetchone()
                await conn.commit()
                return result