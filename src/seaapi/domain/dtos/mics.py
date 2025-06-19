import re
import json
import inspect
from enum import Enum
from datetime import date, datetime
from pydantic import (
    BaseModel,
    ConstrainedStr,
    ConstrainedFloat,
    ConstrainedInt,
    errors,
)
from pydantic.datetime_parse import parse_date
from typing import List, Optional


class OrderField(ConstrainedStr):
    @classmethod
    def validate(cls, value):  # pragma: no cover
        # Verifica se o valor possui o formato desejado
        parts = value.split(",")
        if len(parts) != 2 or parts[1].lower() not in [
            "asc",
            "desc",
        ]:
            raise ValueError(
                f"Formato inválido para campo de ordenação: {value}."
                + " Use campo,asc|desc"
            )

        return value


class SuccessResponse(BaseModel):
    message: str
    code: str
    success: bool = True
    status_code: int = 200


class SuccessWithWarningResponse(SuccessResponse):
    warnings: List[str]


class SuccessWithIdResponse(SuccessResponse):
    reference_id: int
    tempo_slot_config: int


class PaginationParams(BaseModel):
    page: Optional[int] = 1
    page_size: int = 10
    search: Optional[str]
    order: Optional[OrderField]


class PaginationOptions(BaseModel):
    page: int
    pages: int
    results: int
    size: int


class PaginationData(BaseModel):
    data: List
    options: PaginationOptions


class ZipCode(ConstrainedStr):
    min = 8
    max = 8
    regex = r"^\d{5}-?\d{3}$"


class DayOfWeek(ConstrainedInt):
    min = 1
    max = 7

    @classmethod
    def validate(cls, value):  # pragma: no cover
        if value < cls.min or value > cls.max:
            raise ValueError(
                "O dia da semana deve ser um número entre 1 e 7."
            )
        return value


class StrongPassword(ConstrainedStr):
    min = 8
    max = 32
    regex = r"^(?=.*\d)(?=.*[a-z])(?=.*[A-Z])(?=.*[\W_]).*$"

    @classmethod
    def validate(cls, value):
        if len(value) < cls.min:
            raise ValueError(
                "A senha deve ter no mínimo 8 caracteres."
            )
        if len(value) > cls.max:
            raise ValueError(
                "A senha deve ter no máximo 32 caracteres."
            )
        if not re.match(cls.regex, value):
            raise ValueError(
                "A senha deve conter pelo menos um dígito, uma letra minúscula, "
                + "uma letra maiúscula e um caractere especial."
            )
        return value


class GenericGraphPoint(BaseModel):
    data: date
    quantidade: int


class PhoneNumber(ConstrainedStr):
    regex_phone = r"\d{10,11}"

    @classmethod
    def validate(cls, value):  # pragma: no cover
        clean_value = re.sub(r"[^\d]", "", value)

        if not re.match(cls.regex_phone, clean_value):
            raise ValueError(
                "Número de telefone inválido. Deve conter entre 10 e 11 dígitos."
            )
        return value


class CNPJCPF(ConstrainedStr):
    regex_cpf = r"\d{11}"
    regex_cnpj = r"\d{14}"

    @classmethod
    def validate(cls, value):
        clean_value = re.sub(r"[^\d]", "", value)

        if len(clean_value) == 11:
            if not re.match(cls.regex_cpf, clean_value):
                raise ValueError(
                    "CPF inválido. Deve conter exatamente 11 dígitos."
                )
        elif len(clean_value) == 14:
            if not re.match(cls.regex_cnpj, clean_value):
                raise ValueError(
                    "CNPJ inválido. Deve conter exatamente 14 dígitos."
                )
        else:
            raise ValueError(
                "O valor deve ser um CPF ou CNPJ válido."
            )
        return value


class CPF(ConstrainedStr):
    regex_cpf = r"\d{11}"

    @classmethod
    def validate(cls, value):
        clean_value = re.sub(r"[^\d]", "", value)

        if len(clean_value) == 11:
            if not re.match(cls.regex_cpf, clean_value):
                raise ValueError(
                    "CPF inválido. Deve conter exatamente 11 dígitos."
                )
        else:
            raise ValueError(
                "O valor deve ser um CPF válido."
            )
        return value


class PositiveInteger(ConstrainedInt):
    gte = 0

    @classmethod
    def validate(cls, value):  # pragma: no cover
        if value < 0:
            raise ValueError(
                "O número deve ser um inteiro positivo."
            )
        return value


class DateInThePastError(errors.PydanticValueError):
    code = "date.not_in_the_past"
    msg_template = "date is in the past"


class FutureOrTodayDate(date):
    @classmethod
    def __get_validators__(cls):
        yield parse_date
        yield cls.validate

    @classmethod
    def validate(cls, value: date) -> date:
        if value < date.today():
            raise DateInThePastError()

        return value


class PositiveIntegerNonZero(ConstrainedInt):
    gt = 0

    @classmethod
    def validate(cls, value):  # pragma: no cover
        if value <= 0:
            raise ValueError(
                "O número deve ser um inteiro positivo maior que zero."
            )
        return value


class PositiveFloat(ConstrainedFloat):
    gte = 0

    @classmethod
    def validate(cls, value):  # pragma: no cover
        if value < 0:
            raise ValueError(
                "O número deve ser um decimal positivo."
            )
        return value


class StrList(ConstrainedStr):
    target_type = None

    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, value):  # pragma: no cover
        if isinstance(value, list):
            return value
        if value is None:
            return value
        values = []
        try:
            values = value.split(",")
        except Exception:
            raise ValueError(
                "Forneça uma lista em uma formato válido."
            )
        if len(values) == 0:
            raise ValueError("A lista não pode ser vazia")
        if cls.target_type is not None:
            for v in values:
                if hasattr(cls.target_type, "__args__"):
                    if v not in cls.target_type.__args__:
                        raise ValueError(
                            f"Apenas os valores "
                            f"{str(cls.target_type.__args__)} são permitidos"
                        )

                elif not isinstance(v, cls.target_type):
                    raise ValueError(
                        "A lista não pode ser adawdwa"
                    )
        return values


class StrDict(ConstrainedStr):
    def __class_getitem__(cls, item):
        class CustomStrDict(ConstrainedStr):
            @classmethod
            def __get_validators__(cls):
                yield cls.validate

            @classmethod
            def validate_type(
                cls, value
            ):  # pragma: no cover
                try:
                    if item == date:
                        instance = datetime.strptime(
                            value, "%Y-%m-%d"
                        ).date()
                    elif item == datetime:
                        instance = datetime.strptime(
                            value, "%Y-%m-%d %H:%M:%S"
                        )
                    else:
                        instance = item(value)
                except (ValueError, TypeError) as e:
                    print(e)
                    raise ValueError(
                        f"invalid {item.__name__} format"
                    )
                return instance

            @classmethod
            def validate(cls, value):  # pragma: no cover
                if isinstance(value, (list, tuple)):
                    return value
                if isinstance(value, item):
                    return value
                if isinstance(value, dict):
                    return value
                try:
                    filters_dict = json.loads(value)
                    operations = Operator.list()
                    for k, v in filters_dict.items():
                        if k not in operations:
                            raise ValueError(
                                "As opções disponiveis para filtro são: %s"
                                % operations
                            )
                        filters_dict[k] = cls.validate_type(
                            v
                        )
                    return filters_dict
                except Exception as e:
                    print(e)
                    return cls.validate_type(value)

        return CustomStrDict


FilterValue = StrDict


default_pagination_params = PaginationParams(
    page_size=10, page=1
)


class UploadedFile(BaseModel):
    content: bytes
    filename: str
    relative_path: str


def partial(*fields):
    def dec(_cls):
        for field in fields:
            _cls.__fields__[field].required = False
        return _cls

    if (
        fields
        and inspect.isclass(fields[0])
        and issubclass(fields[0], BaseModel)
    ):
        cls = fields[0]
        fields = cls.__fields__
        return dec(cls)
    return dec


class Operator(Enum):
    IN = "in"
    NOT_IN = "not_in"
    LTE = "lte"
    LT = "lt"
    GTE = "gte"
    GT = "gt"
    NOT = "not"
    EXACT = "exact"

    @classmethod
    def list(cls):
        return list(map(lambda c: c.value, cls))


class ContractCandidatesPaginationParams(PaginationParams):
    data: date
    programacao_id: Optional[int]
