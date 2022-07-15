import logging

from fastapi import FastAPI

from app.api import ping
from app.db import init_db

logger = logging.getLogger("uvicorn")


def generate_app() -> FastAPI:
    application = FastAPI()

    application.include_router(ping.router)

    return application


app = generate_app()


@app.on_event("startup")
async def startup_event():
    logger.info("Starting up...")
    init_db(app)


@app.on_event("shutdown")
async def shutdown_event():
    logger.info("Shutting Down...")
