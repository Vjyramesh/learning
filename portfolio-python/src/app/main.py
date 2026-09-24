
from contextlib import asynccontextmanager
from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from src.app.config.dynamic_router import init_databases, register_routers
from src.app.config.database import db_manager

class AppLauncher:

    def __init__(self):
        self.app = 'Portfolio App'
        self.version = '1.0.0'

    @staticmethod
    @asynccontextmanager
    async def lifespan(self):
        await db_manager.connect()
        await init_databases()
        yield
        await db_manager.disconnect()

    @staticmethod
    async def validation_exception_handler(request: Request, exc: RequestValidationError):
        return JSONResponse(
            status_code=400,
            content={"error": True, "message": "Payload is required and must be valid", "details": exc.errors()}
        )

    def launch(self):
        print(f"Launching {self.app} version {self.version}")
        app = FastAPI(title=self.app, version=self.version, lifespan=self.lifespan)
        app.add_exception_handler(RequestValidationError, self.validation_exception_handler)
        register_routers(app)
        return app


app = AppLauncher().launch()
