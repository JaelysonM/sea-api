from src.seaapi.domain.entities.base import BaseEntity


class CustomException(Exception):
    def __init__(
        self, detail: str, status_code: int, error_code: str
    ):
        self.error_code = error_code
        self.detail = detail
        self.status_code = status_code


class SystemException(CustomException):
    def __init__(
        self,
        detail: str = "Ocorreu um erro desconhecido",
        status_code: int = 500,
        error_code: str = "unexpected_error",
    ):
        super().__init__(
            detail=detail,
            status_code=status_code,
            error_code=error_code,
        )


class NotAuthenticatedException(CustomException):
    def __init__(
        self,
        detail: str = "Não autenticado",
        status_code: int = 403,
        error_code: str = "not_authenticated",
    ):
        super().__init__(
            detail=detail,
            status_code=status_code,
            error_code=error_code,
        )


class UserNotActiveException(CustomException):
    def __init__(
        self,
        detail: str = "O usuário está inativo.",
        status_code: int = 403,
        error_code: str = "disabled_user",
    ):
        super().__init__(
            detail=detail,
            status_code=status_code,
            error_code=error_code,
        )


class ExpiredTokenException(CustomException):
    def __init__(
        self,
        detail: str = "Token autenticação informado expirado ou inválido",
        status_code: int = 403,
        error_code: str = "invalid_auth_token",
    ):
        super().__init__(
            detail=detail,
            status_code=status_code,
            error_code=error_code,
        )


class ExpiredVerificationTokenException(CustomException):
    def __init__(
        self,
        detail: str = "Token verificação informado expirado ou inválido",
        status_code: int = 403,
        error_code: str = "invalid_verification_token",
    ):
        super().__init__(
            detail=detail,
            status_code=status_code,
            error_code=error_code,
        )


class InvalidCredentialsException(CustomException):
    def __init__(
        self,
        detail: str = "Senha ou email inválidas, tente novamente",
        status_code: int = 401,
        error_code: str = "invalid_credentials",
    ):
        super().__init__(
            detail=detail,
            status_code=status_code,
            error_code=error_code,
        )


class SamePasswordBeforeException(CustomException):
    def __init__(
        self,
        detail: str = "A senha fornecida não pode ser igual a anterior",
        status_code: int = 400,
        error_code: str = "same_password_before",
    ):
        super().__init__(
            detail=detail,
            status_code=status_code,
            error_code=error_code,
        )


class InvalidEntityAssignException(CustomException):
    def __init__(
        self,
        detail: str = "O identificador fornecido não pode ser igual da própria entidade",
        status_code: int = 400,
        error_code: str = "invalid_entity_assign",
    ):
        super().__init__(
            detail=detail,
            status_code=status_code,
            error_code=error_code,
        )


class EntityNotFoundException(CustomException):
    def __init__(
        self,
        detail: str = "A entidade que você estava procurando não existe",
        status_code: int = 404,
        error_code: str = "entity_not_found",
    ):
        super().__init__(
            detail=detail,
            status_code=status_code,
            error_code=error_code,
        )


class EntityNotFoundOrDeletedException(
    EntityNotFoundException
):
    def __init__(
        self,
        entity_name="entidade",
        masculine=True,
        id=None,
        deleted=False,
        entity: BaseEntity = None,
        identifier="com o ID",
    ):

        entity_name = (
            entity.Meta.verbose.lower()
            if hasattr(entity.Meta, "verbose")
            else entity_name
        )
        masculine = (
            entity.Meta.masculine
            if hasattr(entity.Meta, "masculine")
            else masculine
        )

        first_article = "um" if masculine else "uma"
        second_article = "o" if masculine else "a"
        DELETED_MESSAGE = (
            f"As informações apresentadas pertencem à {first_article} {entity_name}"
            + " que já foi removido da base de dados."
        )
        NOT_FOUND_MESSAGE = (
            f"{second_article.upper()} {entity_name} "
            + f"{identifier} {id} não existe"
        )
        super().__init__(
            detail=(
                DELETED_MESSAGE
                if deleted
                else NOT_FOUND_MESSAGE
            )
        )


class UserNotFoundException(CustomException):
    def __init__(
        self,
        detail: str = "O usuário informado não está cadastrado na base de dados",
        status_code: int = 404,
        error_code: str = "user_not_found",
    ):
        super().__init__(
            detail=detail,
            status_code=status_code,
            error_code=error_code,
        )


class EmailExistsException(CustomException):
    def __init__(
        self,
        detail: str = "O e-mail informado já está sendo utilizado no sistema",
        status_code: int = 400,
        error_code: str = "email_exists",
    ):
        super().__init__(
            detail=detail,
            status_code=status_code,
            error_code=error_code,
        )


class IdentifierExistsException(CustomException):
    def __init__(
        self,
        detail: str = "O CNPJ/CPF informado já está sendo utilizado no sistema",
        status_code: int = 400,
        error_code: str = "identifier_exists",
    ):
        super().__init__(
            detail=detail,
            status_code=status_code,
            error_code=error_code,
        )


class EmailExistsInInactiveUserException(CustomException):
    def __init__(
        self,
        detail: str = "Já existe um usuário desativado na base com o email informado. "
        + "Para reativá-lo, vá na lista de usuários e selecione a ação de desbloqueio.",
        status_code: int = 400,
        error_code: str = "email_exists",
    ):
        super().__init__(
            detail=detail,
            status_code=status_code,
            error_code=error_code,
        )


class EntityAlreadyActiveException(CustomException):
    def __init__(
        self,
        detail: str = "A entidade informada já está ativada.",
        status_code: int = 400,
        error_code: str = "already_active",
    ):
        super().__init__(
            detail=detail,
            status_code=status_code,
            error_code=error_code,
        )


class NotAuthorizedException(CustomException):
    def __init__(
        self,
        detail: str = "O usuário não possui permissão para acessar"
        + " a funcionalidade ou executar esta ação.",
        status_code: int = 403,
        error_code: str = "not_permission",
    ):
        super().__init__(
            detail=detail,
            status_code=status_code,
            error_code=error_code,
        )


class FileBadFormatException(CustomException):
    def __init__(
        self,
        detail: str = "O arquivo informado não pode ser processado.",
        status_code: int = 422,
        error_code: str = "file_bad_format",
    ):
        super().__init__(
            detail=detail,
            status_code=status_code,
            error_code=error_code,
        )


class CannotStorageFileException(CustomException):
    def __init__(
        self,
        detail: str = "Não foi possível persitir o arquivo solicitado, "
        + "se o problema persistir contate um suporte.",
        status_code: int = 500,
        error_code: str = "error_on_upload",
    ):
        super().__init__(
            detail=detail,
            status_code=status_code,
            error_code=error_code,
        )


class MealAlreadyInProgressException(CustomException):
    def __init__(
        self,
        detail: str = "Já existe uma refeição em andamento para este usuário.",
        status_code: int = 400,
        error_code: str = "meal_already_in_progress",
    ):
        super().__init__(
            detail=detail,
            status_code=status_code,
            error_code=error_code,
        )


class MealAlreadyFinishedException(CustomException):
    def __init__(
        self,
        detail: str = "A refeição já foi finalizada.",
        status_code: int = 400,
        error_code: str = "meal_already_finished",
    ):
        super().__init__(
            detail=detail,
            status_code=status_code,
            error_code=error_code,
        )
