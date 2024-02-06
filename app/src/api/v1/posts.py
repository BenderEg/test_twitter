from http import HTTPStatus

from fastapi import APIRouter, Depends

from models.posts import PostInModel, PostOutModel
from services.post_service import PostService, get_post_service

router = APIRouter()


@router.post("/", status_code=HTTPStatus.CREATED,
             response_model=PostOutModel)
async def create_post(post_in: PostInModel,
                      post_service: PostService = Depends(get_post_service)) -> PostOutModel:
    post = await post_service.create(post_in.user_id, post_in.header, post_in.content)
    return PostOutModel(**post.dict())