from fastapi import FastAPI

from db import engine
from db.models import Base
from handlers import router


async def on_startup(*_):
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


def get_app():
    app = FastAPI(on_startup=[on_startup])
    app.include_router(router, prefix='/api')
    return app
