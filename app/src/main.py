from contextlib import asynccontextmanager

import uvicorn

from fastapi import FastAPI, Request
from fastapi.responses import ORJSONResponse

from api.v1 import users, subscriptions, posts
from errors.base import BaseError

@asynccontextmanager
async def lifespan(app: FastAPI):

    yield


app = FastAPI(
    title="Twitter APP",
    description="APP для создания и просмотра постов",
    docs_url="/api/openapi",
    openapi_url="/api/openapi.json",
    default_response_class=ORJSONResponse,
    lifespan=lifespan,
)


app.include_router(users.router,
                   prefix='/api/v1/users',
                   tags=['users'])
app.include_router(subscriptions.router,
                   prefix='/api/v1/subscriptions',
                   tags=['subscriptions'])
app.include_router(posts.router,
                   prefix='/api/v1/posts',
                   tags=['posts'])


@app.exception_handler(BaseError)
async def app_exception_handler(request: Request, exc: BaseError):
    return ORJSONResponse(
        status_code=exc.status_code,
        content=exc.detail,
    )


if __name__ == '__main__':
    uvicorn.run(
        'main:app',
        host='127.0.0.1',
        port=8000,
        reload=True
    )