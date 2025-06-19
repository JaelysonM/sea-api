from fastapi.exceptions import RequestValidationError
from pydantic import ValidationError
from fastapi.responses import JSONResponse
from src.siasdapi.domain.ports.shared.exceptions import (
    CustomException,
)
from src.siasdapi.i18n import tr


def register_handlers(app):
    @app.exception_handler(RequestValidationError)
    @app.exception_handler(ValidationError)
    async def validation_exception_handler(request, exc):
        fields = {}
        for error in tr.translate(
            exc.errors(), locale="pt_BR"
        ):
            field = ".".join(
                [
                    str(x)
                    for x in (
                        error["loc"][1:]
                        if len(error["loc"]) >= 2
                        else error["loc"]
                    )
                ]
            )
            fields[field] = error["msg"]
        return JSONResponse(
            content={
                "message": "Campos inválidos",
                "fields": fields,
                "code": "invalid_request",
                "status_code": 400,
            },
            status_code=400,
        )

    @app.exception_handler(CustomException)
    async def http_custom_exception_handler(request, exc):
        return JSONResponse(
            content={
                "message": exc.detail,
                "code": exc.error_code,
                "status_code": exc.status_code,
            },
            status_code=exc.status_code,
        )

    @app.exception_handler(Exception)
    async def http_exception_handler(
        request, exc
    ):  # pragma: no cover
        if isinstance(exc, CustomException):
            return JSONResponse(
                content={
                    "message": exc.detail,
                    "code": exc.error_code,
                    "status_code": exc.status_code,
                },
                status_code=exc.status_code,
            )
        else:
            return JSONResponse(
                content={
                    "message": str(exc),
                    "code": "internal_error",
                    "status_code": 500,
                },
                status_code=500,
            )
