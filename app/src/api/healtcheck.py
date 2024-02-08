from http import HTTPStatus

from fastapi import APIRouter, Response

router = APIRouter()


@router.get(
    "/health/",
    summary="Проверка состояния сервиса",
    response_description="Состояние сервиса",
    status_code=HTTPStatus.OK,
    response_class=Response,
)
def healthcheck():
    """Check if service healthy."""
    return Response(status_code=HTTPStatus.OK)