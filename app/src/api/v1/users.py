from http import HTTPStatus

from fastapi import APIRouter, Depends

from models.users import UserInModel, UserOutModel
from services.user_service import UserService, get_user_service

router = APIRouter()


@router.post("/", status_code=HTTPStatus.CREATED,
             response_model=UserOutModel)
async def create_user(user_in: UserInModel,
                      user_service: UserService = Depends(get_user_service)) -> UserOutModel:
    user = await user_service.create(user_in.name)
    return UserOutModel(**user.dict())