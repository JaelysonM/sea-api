from dependency_injector.wiring import (
    Provide,
    inject,
)
from fastapi import APIRouter, Depends, Response
from fastapi.security import HTTPBearer
from src.seaapi.domain.ports.use_cases.qrcode import (
    QRCodeServiceInterface,
)
from src.seaapi.config.containers import Container
from src.seaapi.domain.dtos.qrcode import (
    QRCodeCreateInputDto,
    QRCodeTokenDto,
    QRCodeRegenerateInputDto,
    QRCodeInfoResponseDto,
)
from src.seaapi.domain.dtos.mics import SuccessResponse
from src.seaapi.domain.dtos.tokens import Tokens
from src.seaapi.adapters.entrypoints.api.shared.permissions import (
    PermissionsDependency,
    And,
    IsAuthenticated,
    IsAdministrator,
)

router = APIRouter()
auth_scheme = HTTPBearer()


@router.post(
    "/create",
    status_code=201,
    dependencies=[
        Depends(
            PermissionsDependency(
                And(
                    [
                        IsAuthenticated(),
                        IsAdministrator(),
                    ]
                )
            )
        ),
        Depends(auth_scheme),
    ],
)
@inject
def create_qrcode_token(
    data: QRCodeCreateInputDto,
    qrcode_service: QRCodeServiceInterface = Depends(
        Provide[Container.qrcode_service]
    ),
) -> Response:
    image_bytes = qrcode_service.create_qrcode_token(data)
    return Response(
        content=image_bytes,
        media_type="image/png",
        headers={
            "Content-Disposition": "inline; filename=qrcode.png",
            "Cache-Control": "no-cache",
        },
    )


@router.post(
    "/regenerate/{token_id}",
    dependencies=[
        Depends(
            PermissionsDependency(
                And(
                    [
                        IsAuthenticated(),
                        IsAdministrator(),
                    ]
                )
            )
        ),
        Depends(auth_scheme),
    ],
)
@inject
def regenerate_qrcode(
    token_id: int,
    data: QRCodeRegenerateInputDto,
    qrcode_service: QRCodeServiceInterface = Depends(
        Provide[Container.qrcode_service]
    ),
) -> Response:
    image_bytes = qrcode_service.regenerate_qrcode(
        token_id, data.frontend_url
    )
    return Response(
        content=image_bytes,
        media_type="image/png",
        headers={
            "Content-Disposition": "inline; filename=qrcode_regenerated.png",
            "Cache-Control": "no-cache",
        },
    )


@router.post(
    "/authenticate",
    response_model=Tokens,
)
@inject
def authenticate_with_qrcode(
    data: QRCodeTokenDto,
    qrcode_service: QRCodeServiceInterface = Depends(
        Provide[Container.qrcode_service]
    ),
):
    return qrcode_service.authenticate_with_qrcode(data)


@router.get(
    "/info/{token_id}",
    response_model=QRCodeInfoResponseDto,
    dependencies=[
        Depends(
            PermissionsDependency(
                And(
                    [
                        IsAuthenticated(),
                        IsAdministrator(),
                    ]
                )
            )
        ),
        Depends(auth_scheme),
    ],
)
@inject
def get_qrcode_info(
    token_id: int,
    qrcode_service: QRCodeServiceInterface = Depends(
        Provide[Container.qrcode_service]
    ),
):
    return qrcode_service.get_qrcode_info(token_id)


@router.delete(
    "/revoke/{token_id}",
    status_code=200,
    response_model=SuccessResponse,
    dependencies=[
        Depends(
            PermissionsDependency(
                And(
                    [
                        IsAuthenticated(),
                        IsAdministrator(),
                    ]
                )
            )
        ),
        Depends(auth_scheme),
    ],
)
@inject
def revoke_qrcode_token(
    token_id: int,
    qrcode_service: QRCodeServiceInterface = Depends(
        Provide[Container.qrcode_service]
    ),
):
    return qrcode_service.revoke_token(token_id)
