from pydantic_i18n import PydanticI18n

from src.seaapi.i18n.locales import pt_BR


tr = PydanticI18n(
    {
        "pt_BR": pt_BR,
    },
    default_locale="pt_BR",
)
