from contextlib import asynccontextmanager

import uvicorn

from fastapi import FastAPI, Request
from fastapi.responses import ORJSONResponse
from redis.asyncio import Redis

from api import healtcheck
from api.v1 import users, subscriptions, posts
from background.regular import scheduler
from core.config import settings
from db import red_conn
from errors.base import BaseError
from partition.partitioning import create_partioning_tables

@asynccontextmanager
async def lifespan(app: FastAPI):
    red_conn.redis = Redis(host=settings.redis.host,
                           port=settings.redis.port,
                           db=settings.redis.db,
                           encoding="utf-8",
                           decode_responses=True
                           )
    scheduler.start()
    await create_partioning_tables(settings.feed_partitions, "feeds")
    yield
    scheduler.shutdown()
    await red_conn.redis.close()


app = FastAPI(
    title="Twitter APP",
    description="APP для создания и просмотра постов",
    docs_url="/api/openapi",
    openapi_url="/api/openapi.json",
    default_response_class=ORJSONResponse,
    lifespan=lifespan,
)

app.include_router(users.router, prefix="/api/v1/users", tags=["Пользователи"])
app.include_router(subscriptions.router, prefix="/api/v1/subscriptions", tags=["Подписки"])
app.include_router(posts.router, prefix="/api/v1/posts", tags=["Посты"])
app.include_router(healtcheck.router, tags=["Проверка состояния"])

@app.exception_handler(BaseError)
async def app_exception_handler(request: Request, exc: BaseError):
    return ORJSONResponse(
        status_code=exc.status_code,
        content=exc.detail,
    )


if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="127.0.0.1",
        port=8000,
        reload=True
    )