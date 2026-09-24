from pathlib import Path
import importlib
from fastapi import FastAPI
import inspect
from src.app.config.database import db_manager

def register_routers(app: FastAPI) -> None:
    modules_dir = Path(__file__).resolve().parent.parent / "modules"
    for entry in modules_dir.iterdir():
        if not entry.is_dir():
            continue
        if not (entry / "router.py").exists():
            continue

        module_name = entry.name
        router_module = importlib.import_module(
            f"src.app.modules.{module_name}.router"
        )
        router = getattr(router_module, "router", None)
        if router is not None:
            app.include_router(router)


async def init_databases() -> None:
    modules_dir = Path(__file__).resolve().parent.parent / "modules"
    for entry in modules_dir.iterdir():
        if not entry.is_dir():
            continue
        if not (entry / "repository.py").exists():
            continue

        repo_module = importlib.import_module(
            f"src.app.modules.{entry.name}.repository"
        )

        for _, obj in inspect.getmembers(repo_module, inspect.isclass):
            if obj.__module__ == repo_module.__name__ and hasattr(obj, "init"):
                repository = obj(db=db_manager)
                await repository.init()