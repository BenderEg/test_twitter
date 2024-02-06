from contextlib import asynccontextmanager

import uvicorn

from fastapi import FastAPI
from fastapi.responses import ORJSONResponse

from api.v1 import users, subscriptions, posts


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


if __name__ == '__main__':
    uvicorn.run(
        'main:app',
        host='127.0.0.1',
        port=8000,
        reload=True
    )