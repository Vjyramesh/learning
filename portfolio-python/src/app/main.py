
from contextlib import asynccontextmanager
from fastapi import FastAPI
from src.app.config.dynamic_router import register_routers
from src.app.config.database import db_manager

class AppLauncher:

    def __init__(self):
        self.app = 'Portfolio App'
        self.version = '1.0.0'

    @staticmethod
    @asynccontextmanager
    async def lifespan(self):
        await db_manager.connect()
        yield
        await db_manager.disconnect()

    def launch(self):
        print(f"Launching {self.app} version {self.version}")
        app = FastAPI(title=self.app, version=self.version, lifespan=self.lifespan)
        register_routers(app)
        return app


app = AppLauncher().launch()
