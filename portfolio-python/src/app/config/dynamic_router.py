from pathlib import Path
import importlib
from fastapi import FastAPI

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
