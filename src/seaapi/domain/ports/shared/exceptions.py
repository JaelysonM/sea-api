from typing import List
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


class FanLogDateExistsException(CustomException):
    def __init__(
        self,
        detail: str = (
            "Foi registrado no mesmo um log "
            + "do FAN, tente novamente em alguns segundos"
        ),
        status_code: int = 400,
        error_code: str = "fan_log_exists",
    ):
        super().__init__(
            detail=detail,
            status_code=status_code,
            error_code=error_code,
        )


class FanSerialExistsException(CustomException):
    def __init__(
        self,
        detail: str = "O serial informado para esse FAN já está sendo utilizado",
        status_code: int = 400,
        error_code: str = "fan_serial_exists",
    ):
        super().__init__(
            detail=detail,
            status_code=status_code,
            error_code=error_code,
        )


class FanWithAnPendingCommandException(CustomException):
    def __init__(self, serial: str = ""):
        super().__init__(
            detail="O Fan #%s já está com um comando pendente."
            % (serial),
            status_code=400,
            error_code="fan_with_pending_command",
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


class PleaseProvideAnCustomerException(CustomException):
    def __init__(
        self,
        detail: str = "É necessário fornecer algum cliente para executar esta ação.",
        status_code: int = 400,
        error_code: str = "undefined_customer",
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


class InvalidVideoDurationException(CustomException):
    def __init__(
        self,
        detail: str = "O arquivo de vídeo enviado possui a duração "
        + "maior que o permitido.",
        status_code: int = 400,
        error_code: str = "invalid_video_duration",
    ):
        super().__init__(
            detail=detail,
            status_code=status_code,
            error_code=error_code,
        )


class InvalidVideoSizeException(CustomException):
    def __init__(
        self,
        max_size: str,
        status_code: int = 400,
        error_code: str = "invalid_video_size",
    ):
        super().__init__(
            detail=f"O tamanho máximo do vídeo deve ser {max_size}",
            status_code=status_code,
            error_code=error_code,
        )


class InvalidVideoFormatException(CustomException):
    def __init__(
        self,
        width: int,
        height: int,
        fps: int,
        status_code: int = 400,
        error_code: str = "invalid_video_format",
    ):
        super().__init__(
            detail="Formato de vídeo inválido. "
            f"Aceito: {width}x{height} pixels à {fps}fps e até 16 bits de cor.",
            status_code=status_code,
            error_code=error_code,
        )


class NotPermittedInVideoStatusException(CustomException):
    def __init__(
        self,
        detail: str = "Apenas é possível aprovar/reprovar um "
        + "vídeo no qual o status é 'Cadastrado'",
        status_code: int = 400,
        error_code: str = "not_permitted_video_status",
    ):
        super().__init__(
            detail=detail,
            status_code=status_code,
            error_code=error_code,
        )


class BusyFansException(CustomException):
    def __init__(
        self,
        fans: List[str],
        status_code: int = 400,
        error_code: str = "busy_fans",
    ):
        joined_fans = ", ".join(fans)
        super().__init__(
            detail=f"Os FANs: '{joined_fans}' possuem "
            + "um contrato de instalação em vigência.",
            status_code=status_code,
            error_code=error_code,
        )


class FansUsageValidationException(CustomException):
    def __init__(
        self,
        errors: List[str],
        status_code: int = 400,
        error_code: str = "fans_usage_validation_error",
    ):
        super().__init__(
            detail=errors,
            status_code=status_code,
            error_code=error_code,
        )


class EmptyFansException(CustomException):
    def __init__(
        self,
        status_code: int = 400,
        error_code: str = "empty_fans",
    ):
        super().__init__(
            detail="Forneça pelo menos um FAN",
            status_code=status_code,
            error_code=error_code,
        )


class InvalidContractPercentageException(CustomException):
    def __init__(
        self,
        status_code: int = 400,
        error_code: str = "invalid_contract_percentage",
    ):
        super().__init__(
            detail="O soma do percentual MaV e Local deve ser igual à 100%",
            status_code=status_code,
            error_code=error_code,
        )


class InvalidContractPeriodException(CustomException):
    def __init__(
        self,
        status_code: int = 400,
        error_code: str = "invalid_contract_period",
    ):
        super().__init__(
            detail="Período de contrato inválido, a data de fim "
            "deve ser maior que data de início.",
            status_code=status_code,
            error_code=error_code,
        )


class InvalidContractParamsException(CustomException):
    def __init__(
        self,
        status_code: int = 400,
        error_code: str = "invalid_contract_params",
    ):
        super().__init__(
            detail="Os paramêtros são inválidos estes devem seguir a seguinte equação: "
            "Número de inserções diárias = ⌊Número de Inserções totais/Quantidade de "
            "dias do contrato⌋",
            status_code=status_code,
            error_code=error_code,
        )


class InvalidContractInScheduleException(CustomException):
    def __init__(
        self,
        contracts: List[int],
        status_code: int = 400,
        error_code: str = "invalid_contract_in_schedule",
        contract_type: str = "instalação",
    ):
        joined_contracts = ", ".join(
            [f"#{c}" for c in contracts]
        )
        super().__init__(
            detail=f"Os contratos de {contract_type} com IDs: {joined_contracts} "
            "estão em alguma programação no dia ou o seu intervalo não abrange "
            "a data da programação.",
            status_code=status_code,
            error_code=error_code,
        )


class CannotEditCompletedScheduleException(CustomException):
    def __init__(
        self,
        detail: str = "Não é possível editar uma programação que já foi concluída.",
        status_code: int = 400,
        error_code: str = "completed_schedule",
    ):
        super().__init__(
            detail=detail,
            status_code=status_code,
            error_code=error_code,
        )


class ScheduleAlreadyConsolidatedException(CustomException):
    def __init__(
        self,
        detail: str = "Não é possível consolidar uma programação que já foi consolidada",
        status_code: int = 400,
        error_code: str = "schedule_already_consolidated",
    ):
        super().__init__(
            detail=detail,
            status_code=status_code,
            error_code=error_code,
        )


class CannotConsolidateExpiredScheduleException(
    CustomException
):
    def __init__(
        self,
        detail: str = "Não é possível consolidar uma programação que com a "
        "data antiga.",
        status_code: int = 400,
        error_code: str = "can_consolidate_expired_schedule",
    ):
        super().__init__(
            detail=detail,
            status_code=status_code,
            error_code=error_code,
        )


class CannotConsolidateScheduleWithoutContractsException(
    CustomException
):
    def __init__(
        self,
        detail: str = "Não é possível consolidar uma programação sem contratos.",
        status_code: int = 400,
        error_code: str = "can_consolidate_schedule_without_contracts",
    ):
        super().__init__(
            detail=detail,
            status_code=status_code,
            error_code=error_code,
        )


class CannotPausedNotRunningScheduleException(
    CustomException
):
    def __init__(
        self,
        detail: str = "Não é possível interromper uma programação que "
        "não está em execução.",
        status_code: int = 400,
        error_code: str = "can_paused_schedule_not_running_schedule",
    ):
        super().__init__(
            detail=detail,
            status_code=status_code,
            error_code=error_code,
        )


class ActiveSchedulesException(CustomException):
    def __init__(
        self,
        detail: str = "Há programações ativas ou em processo de edição "
        "tanto para o futuro quanto para o dia de hoje.",
        status_code: int = 401,
        error_code: str = "active_schedules",
    ):
        super().__init__(
            detail=detail,
            status_code=status_code,
            error_code=error_code,
        )


class OutOfRangeSlotsException(CustomException):
    def __init__(
        self,
        max_slots: int,
        status_code: int = 400,
        error_code: str = "out_of_range_slot",
    ):
        super().__init__(
            detail="Não é possível alocar este slot pois o valor "
            f"máximo do slot é {max_slots}.",
            status_code=status_code,
            error_code=error_code,
        )


class OutOfCapacitySlotsException(CustomException):
    def __init__(
        self,
        detail: str = "Não é possível alocar este slot pois chegou na capacidade"
        " máxima disponível para o FAN no contrato.",
        status_code: int = 400,
        error_code: str = "out_of_capacity_slots",
    ):
        super().__init__(
            detail=detail,
            status_code=status_code,
            error_code=error_code,
        )


class InstallationContractNotExistsInScheduleException(
    CustomException
):
    def __init__(
        self,
        detail: str = "O contrato de instalação informado não existe na programação.",
        status_code: int = 400,
        error_code: str = "installation_contract_not_exists_in_schedule",
    ):
        super().__init__(
            detail=detail,
            status_code=status_code,
            error_code=error_code,
        )


class AdvertisingContractNotExistsInScheduleException(
    CustomException
):
    def __init__(
        self,
        detail: str = "O contrato de publicidade informado não existe na programação.",
        status_code: int = 400,
        error_code: str = "advertising_contract_not_exists_in_schedule",
    ):
        super().__init__(
            detail=detail,
            status_code=status_code,
            error_code=error_code,
        )


class BusySlotInFanScheduleException(CustomException):
    def __init__(
        self,
        slot: int,
        status_code: int = 401,
        error_code: str = "busy_slot_in_fan_schedule",
    ):
        super().__init__(
            detail=f"O slot {slot} do FAN já está ocupado por "
            "um contrato diferente nesta ou em outra programação desta data.",
            status_code=status_code,
            error_code=error_code,
        )


class InvalidFanInContractException(CustomException):
    def __init__(
        self,
        detail: str = "O FAN informado não faz parte desse contrado.",
        status_code: int = 401,
        error_code: str = "invalid_fan_in_contract",
    ):
        super().__init__(
            detail=detail,
            status_code=status_code,
            error_code=error_code,
        )


class ContractWithScheduleRestrictionException(
    CustomException
):
    def __init__(
        self,
        detail: List[str] = [],
        status_code: int = 401,
        error_code: str = "contract_with_schedule_restriction",
    ):
        super().__init__(
            detail=detail,
            status_code=status_code,
            error_code=error_code,
        )


class CustomerWithContractsException(CustomException):
    def __init__(
        self,
        detail: str = "Não é possível remover um cliente que possui contratos vigentes"
        " ou planejados",
        status_code: int = 401,
        error_code: str = "customer_with_contracts",
    ):
        super().__init__(
            detail=detail,
            status_code=status_code,
            error_code=error_code,
        )


class ContractWithScheduleException(CustomException):
    def __init__(
        self,
        detail: str = "Não é possível remover um contrato que está em programações "
        "criadas",
        status_code: int = 401,
        error_code: str = "customer_with_contracts",
    ):
        super().__init__(
            detail=detail,
            status_code=status_code,
            error_code=error_code,
        )


class EmptyScheduleVersionsException(CustomException):
    def __init__(
        self,
        detail: str = "Não há versões de programação para a data informada",
        status_code: int = 404,
        error_code: str = "empty_schedule_version",
    ):
        super().__init__(
            detail=detail,
            status_code=status_code,
            error_code=error_code,
        )


class FanScheduleVersionNotFoundException(CustomException):
    def __init__(
        self,
        detail: str = "Não foi encontrada uma versão de programação com "
        "os valores informados",
        status_code: int = 404,
        error_code: str = "entity_not_found",
    ):
        super().__init__(
            detail=detail,
            status_code=status_code,
            error_code=error_code,
        )


class MaxSlotCapacityException(CustomException):
    def __init__(
        self,
        max_slots: int,
        status_code: int = 400,
        error_code: str = "max_slots_capacity",
    ):
        super().__init__(
            detail=f"A quantidade máxima de slots permitida é {max_slots}.",
            status_code=status_code,
            error_code=error_code,
        )


class InvalidFanTimePeriodException(CustomException):
    def __init__(
        self,
        fan_id: str,
        status_code: int = 400,
        error_code: str = "invalid_fan_time_period",
    ):
        super().__init__(
            detail=f"Período de funcionamento do FAN #{fan_id} inválido"
            ", a hora de fim deve ser maior que hora de início.",
            status_code=status_code,
            error_code=error_code,
        )


class NotUsableInVideoStatusException(CustomException):
    def __init__(
        self,
        detail: str = "Apenas é possível alocar um "
        + "vídeo no qual o status é 'Aceito'",
        status_code: int = 400,
        error_code: str = "not_usable_video_status",
    ):
        super().__init__(
            detail=detail,
            status_code=status_code,
            error_code=error_code,
        )


class FanSensorErrorException(CustomException):
    def __init__(
        self,
        detail: str = "Ocorreu um erro ao ler os dados dos sensores, "
        "forneça as chaves: medida, unidade, cor",
        status_code: int = 400,
        error_code: str = "fan_sensor_error",
    ):
        super().__init__(
            detail=detail,
            status_code=status_code,
            error_code=error_code,
        )


class InvalidFanStatusException(CustomException):
    def __init__(
        self,
        detail: str = "O intervalo de valor para status do FAN deve ser entre [1, 5]",
        status_code: int = 400,
        error_code: str = "invalid_fan_status",
    ):
        super().__init__(
            detail=detail,
            status_code=status_code,
            error_code=error_code,
        )


class ContractIntegrityRestrictionException(
    CustomException
):
    def __init__(
        self,
        detail: List[str] = [],
        status_code: int = 401,
        error_code: str = "contract_integrity_restriction",
    ):
        super().__init__(
            detail=detail,
            status_code=status_code,
            error_code=error_code,
        )


class FanWithoutContractException(CustomException):
    def __init__(
        self,
        status_code: int = 403,
        error_code: str = "fan_without_contract",
    ):
        super().__init__(
            detail="O FAN não possui um contrato de instalação ativo",
            status_code=status_code,
            error_code=error_code,
        )
