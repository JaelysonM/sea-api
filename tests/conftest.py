import pytest
import os
from typing import Any, Generator
from datetime import datetime, timedelta, date
from fastapi import FastAPI
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from src.seaapi.adapters.db.orm import metadata
from src.seaapi.adapters.entrypoints.application import (
    app as original_app,
)
from src.seaapi.config.settings import settings
from tests.fake_container import Container
from tests.utils.auth import (
    authentication_token_from_superuser,
    refresh_token_from_superuser,
)
from tests.utils.video import (
    create_fake_video_and_temporary_file,
)

engine = create_engine(
    settings.TEST_DATABASE_URL,
    connect_args={"check_same_thread": False},
)
# Use connect_args parameter only with sqlite
SessionTesting = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
)

migrations_applied = False


def delete_database_file():
    if settings.TEST_DATABASE_URL.startswith("sqlite:///"):
        db_file = settings.TEST_DATABASE_URL[
            len("sqlite:///") :
        ]

        if os.path.isfile(db_file):
            os.remove(db_file)


@pytest.fixture(scope="package")
def get_fake_container():
    return Container()


@pytest.fixture(scope="package")
def app():
    metadata.create_all(engine)
    yield original_app
    metadata.drop_all(engine)
    delete_database_file()


@pytest.fixture
def get_user_model_dict():
    now = datetime.now()
    return {
        "id": 1,
        "first_name": "3D-Fans",
        "last_name": "QA",
        "email": "testing@3dfans.com.br",
        "password": "password",
        "is_active": True,
        "is_super_user": False,
        "cliente_id": None,
        "created_at": now,
        "updated_at": now,
        "deleted_at": None,
        "last_login": now,
    }


@pytest.fixture
def get_create_user_dict():
    return {
        "first_name": "Joseph",
        "last_name": "Tester",
        "email": "joseph@tester.com",
        "password": "D4ntForgotPass#",
    }


@pytest.fixture
def get_create_group_dict():
    return {
        "name": "QA",
        "default": False,
        "permissions": [1],
    }


@pytest.fixture
def get_create_customer_dict():
    return {
        "nome": "QA Customer",
        "cep": "00020000",
        "logradouro": "St QA",
        "bairro": "QA Neighbor",
        "cidade_id": 1,
        "numero": "1",
        "ativo": True,
        "tipos": [1],
    }


@pytest.fixture
def get_create_video_dict():
    return {
        "nome": "Test Video",
        "descricao": "An testing video",
        "cliente_id": 1,
    }


@pytest.fixture
def get_fake_video():
    fake_video = create_fake_video_and_temporary_file(
        duration_seconds=1, fps=24, height=1024, width=1024
    )
    return ("fake_video.mp4", fake_video, "video/mp4")


@pytest.fixture
def get_fake_video_bytes():
    fake_video = create_fake_video_and_temporary_file(
        duration_seconds=1, fps=24, height=1024, width=1024
    )
    return ("fake_video.mp4", fake_video, "video/mp4")


@pytest.fixture
def get_large_fake_video():
    fake_video = create_fake_video_and_temporary_file(
        duration_seconds=50, fps=24, height=1024, width=1024
    )
    return ("large_fake_video.mp4", fake_video, "video/mp4")


@pytest.fixture
def get_invalid_fake_video():
    fake_video = create_fake_video_and_temporary_file(
        duration_seconds=1, fps=60, height=1920, width=1080
    )
    return (
        "invalid_fake_video.mp4",
        fake_video,
        "video/mp4",
    )


@pytest.fixture
def get_big_fake_video():
    fake_video = create_fake_video_and_temporary_file(
        duration_seconds=40, fps=60, height=1920, width=1920
    )
    return ("big+fake_video.mp4", fake_video, "video/mp4")


@pytest.fixture
def get_update_customer_dict():
    return {"nome": "QA Customer 1 CHG", "tipos": []}


@pytest.fixture
def get_update_customer_type_dict():
    return {
        "nome": "QA Customer Type 1 CHG",
        "bloqueios": [2],
    }


@pytest.fixture
def get_update_video_dict():
    return {
        "nome": "New QA Video",
        "descricao": "Another description",
    }


@pytest.fixture
def get_analyze_reject_video_dict():
    return {
        "aceito": False,
        "justificativa": "Because I want",
    }


@pytest.fixture
def get_analyze_accept_video_dict():
    return {
        "aceito": True,
    }


@pytest.fixture
def get_create_customer_type_dict():
    return {"nome": "QAs", "ativo": True, "bloqueios": []}


@pytest.fixture
def get_create_fan_dict():
    return {
        "serial": "FAN-QA1",
        "nome": "Testing Fan",
        "x_coord": 255,
        "y_coord": -255,
    }


@pytest.fixture
def get_create_fan_log_command_dict():
    return {
        "descricao": "Turn off FAN",
        "dados": None,
        "codigo_evento": "cmd",
    }


@pytest.fixture
def get_create_fan_log_fail_dict():
    return {
        "descricao": "Energia acabou",
        "dados": None,
        "codigo_evento": "falha",
    }


@pytest.fixture
def get_create_fan_log_status_dict():
    return {
        "descricao": "Energia acabou",
        "dados": {"status": 1},
        "codigo_evento": "status",
    }


@pytest.fixture
def get_create_fan_schedule_count():
    return {
        "data": "2024-01-14",
        "contratos": [
            {
                "contrato_tipo": "instalacao",
                "contrato_id": 1,
                "video_id": 1,
                "quantidade": 567,
            },
            {
                "contrato_tipo": "publicidade",
                "contrato_id": 1,
                "video_id": 1,
                "quantidade": 554,
            },
        ],
    }


@pytest.fixture
def get_execute_fan_dict():
    return {"comando": "turn_on"}


@pytest.fixture
def get_update_group_dict():
    return {
        "name": "QA Update",
        "default": True,
        "permissions": [],
    }


@pytest.fixture
def get_update_user_dict():
    return {
        "first_name": "Super Super",
        "last_name": "User",
        "email": "super@3dfans.com",
        "password": "D4ntForgotPass#V2",
    }


@pytest.fixture
def get_update_auth_user_dict():
    return {
        "first_name": "Super",
        "last_name": "User",
        "cidade_id": 3501,
    }


@pytest.fixture
def get_update_parameters_dict():
    return {"tempo_slot": 5, "qtd_slots_loop": 10}


@pytest.fixture
def get_update_parameters_with_out_of_slots_dict():
    return {
        "qtd_slots_loop": int(settings.MAX_VIDEO_SLOTS) + 2
    }


@pytest.fixture
def get_permission_model_dict():
    return {
        "id": 1,
        "code": "create_user",
        "name": "Create User",
    }


@pytest.fixture
def get_token_model_dict():
    now = datetime.now()
    return {
        "id": 1,
        "type": "testing",
        "token": "7203a95d-7d16-4884-982a-94514f607281",
        "reference": 1,
        "expiration": now + timedelta(seconds=30),
        "created_at": now,
    }


@pytest.fixture
def get_group_model_dict():
    return {
        "id": 1,
        "name": "QA",
        "default": False,
    }


@pytest.fixture
def get_city_model_dict():
    return {
        "id": 1,
        "nome": "Fortaleza",
        "ibge": "9990",
        "uf_id": 1,
    }


@pytest.fixture
def get_state_model_dict():
    return {
        "id": 999,
        "nome": "MyState",
        "sigla": "MY",
    }


@pytest.fixture
def get_customer_model_dict():
    now = datetime.now()
    return {
        "id": 1,
        "nome": "QA Customer",
        "cep": "00020000",
        "logradouro": "St QA",
        "bairro": "QA Neighbor",
        "cidade_id": 1,
        "numero": "1",
        "ativo": True,
        "created_at": now,
        "updated_at": now,
        "deleted_at": None,
    }


@pytest.fixture
def get_customer_type_model_dict():
    now = datetime.now()
    return {
        "id": 1,
        "nome": "QA Customer Type",
        "ativo": True,
        "created_at": now,
        "updated_at": now,
        "deleted_at": None,
    }


@pytest.fixture
def get_fan_model_dict():
    now = datetime.now()
    return {
        "id": 1,
        "serial": "FAN-QA1",
        "nome": "Testing Fan",
        "status": 1,
        "comando": None,
        "x_coord": 255,
        "y_coord": -255,
        "created_at": now,
        "updated_at": now,
    }


@pytest.fixture
def get_fan_log_model_dict():
    now = datetime.now()
    return {
        "data_hora": now,
        "fan_id": 1,
        "descricao": "Fan temperature is: 60 Celsius",
        "dados": {"temperature": 60},
        "codigo_evento": "sensors",
    }


@pytest.fixture
def get_fan_sensor_model_dict():
    now = datetime.now()
    return {
        "sensor": "temperatura",
        "fan_id": 1,
        "medida": "56",
        "unidade": "C",
        "cor": "#000000",
    }


@pytest.fixture
def get_video_model_dict():
    now = datetime.now()
    return {
        "id": 1,
        "nome": "QA testing",
        "descricao": "An testing video",
        "url_arquivo": "path/to/video.mp4",
        "url_arquivo_alt": "path/to/alt_video.mp4",
        "data_upload": now,
        "duracao": 100,
        "status": "CAD",
        "largura_px": 500,
        "altura_px": 500,
        "fps": 60,
        "cliente_id": 1,
        "justificativa": None,
        "usuario_analise_id": None,
        "data_analise": None,
        "created_at": now,
        "updated_at": now,
        "deleted_at": None,
    }


@pytest.fixture
def get_installation_contract_model_dict():
    now = datetime.now()
    return {
        "id": 1,
        "data_inicio": datetime(
            year=2024, month=1, day=1
        ).date,
        "data_fim": datetime(
            year=2024, month=1, day=1
        ).date,
        "percentual_local": 50,
        "percentual_mav": 50,
        "cliente_id": 1,
        "created_at": now,
        "updated_at": now,
        "deleted_at": None,
        "ativo": True,
    }


@pytest.fixture
def get_installation_contract_fan_model_dict():
    return {
        "contrato_id": 1,
        "fan_id": 1,
        "hora_inicio": "7:00",
        "hora_fim": "12:00",
    }


@pytest.fixture
def get_advertising_contract_fan_model_dict():
    return {
        "contrato_id": 1,
        "fan_id": 1,
        "numero_slots": 3,
    }


@pytest.fixture
def get_create_fan_log_dict():
    return {
        "descricao": "Fan temperature is: 60 Celsius",
        "dados": {"temperature": 60},
        "codigo_evento": "sensors",
    }


@pytest.fixture
def get_parameters_model_dict():
    return {
        "id": 1,
        "tempo_slot": 5,
        "tempo_offline": 10,
        "qtd_slots_loop": 5,
    }


@pytest.fixture
def get_fan_schedule_model_dict():
    now = datetime.now()
    return {
        "fan_id": 1,
        "data": now.date(),
        "versao": now,
        "entrega": None,
    }


@pytest.fixture
def get_video_schedule_model_dict():
    return {
        "fan_id": 1,
        "slot": 1,
        "programacao_id": 1,
        "contrato_instalacao_id": 1,
        "contrato_publicidade_id": None,
        "video_id": 1,
    }


@pytest.fixture
def get_schedule_model_dict():
    now = datetime.now()
    return {
        "id": 1,
        "data": now.date(),
        "qtd_slots_config": 7,
        "tempo_slot_config": 20,
        "total_videos": 0,
        "total_videos_alocados": 0,
        "consolidada": False,
        "pausada": False,
        "ativo": True,
        "created_at": now,
        "updated_at": now,
        "deleted_at": None,
    }


@pytest.fixture
def get_installation_contract_insertion_model_dict():
    now = date.today()
    return {
        "contrato_instalacao_id": 1,
        "fan_id": 1,
        "data": now,
        "video_id": 1,
        "quantidade": 100,
    }


@pytest.fixture
def get_advertising_contract_insertion_model_dict():
    now = date.today()
    return {
        "contrato_publicidade_id": 1,
        "fan_id": 1,
        "data": now,
        "video_id": 1,
        "quantidade": 100,
    }


@pytest.fixture
def get_installation_contract_schedule_model_dict():
    return {
        "programacao_id": 1,
        "contrato_instalacao_id": 1,
    }


@pytest.fixture
def get_advertising_contract_schedule_model_dict():
    return {
        "programacao_id": 1,
        "contrato_publicidade_id": 1,
    }


@pytest.fixture
def get_create_installation_contract_dict():
    return {
        "data_inicio": "2024-01-01",
        "data_fim": "2024-01-31",
        "percentual_local": 50,
        "percentual_mav": 50,
        "cliente_id": 1,
        "fans": [
            {
                "fan_id": 1,
                "hora_inicio": "07:30",
                "hora_fim": "16:00",
            },
            {
                "fan_id": 2,
                "hora_inicio": "07:30",
                "hora_fim": "20:00",
            },
        ],
    }


@pytest.fixture
def get_create_installation_contract_alt_fans_dict():
    return [
        {
            "fan_id": 3,
            "hora_inicio": "07:30",
            "hora_fim": "16:00",
        }
    ]


@pytest.fixture
def get_update_installation_contract_dict():
    return {
        "fans": [
            {
                "fan_id": 1,
                "hora_inicio": "07:00",
                "hora_fim": "15:00",
            }
        ],
    }


@pytest.fixture
def get_create_advertising_contract_dict():
    return {
        "data_inicio": "2024-01-13",
        "data_fim": "2024-01-15",
        "numero_insercoes_diarias": 50,
        "numero_total_insercoes": 150,
        "cliente_id": 2,
        "fans": [{"fan_id": 1, "numero_slots": 2}],
    }


@pytest.fixture
def get_create_advertising_contract_alt_fans_dict():
    return [{"fan_id": 3, "numero_slots": 4}]


@pytest.fixture
def get_update_advertising_contract_dict():
    return {
        "fans": [
            {
                "fan_id": 1,
                "numero_slots": 3,
            }
        ],
    }


@pytest.fixture
def get_create_schedule_dict():
    return {"data": "2024-01-13"}


@pytest.fixture
def get_update_schedule_date_dict():
    return {"data": "2024-01-15"}


@pytest.fixture
def get_update_consolidated_schedule_date_dict():
    return {"data": "2024-01-14"}


@pytest.fixture
def get_update_schedule_update_contract_dict():
    return {
        "contratos_publicidade": [],
        "contratos_instalacao": [],
    }


@pytest.fixture
def get_update_schedule_date_out_inst_contracts_dict():
    return {"data": "2024-02-01"}


@pytest.fixture
def get_update_schedule_date_out_ad_contracts_dict():
    return {"data": "2024-01-16"}


@pytest.fixture
def get_update_completed_schedule_dict():
    return {"data": "2024-02-15"}


@pytest.fixture
def get_allocate_video_schedule_in_installation_dict():
    return {
        "fan_id": 1,
        "video_id": 1,
        "slot": 1,
        "contrato_instalacao_id": 1,
    }


@pytest.fixture
def get_allocate_video_schedule_in_advertising_dict():
    return {
        "fan_id": 1,
        "video_id": 1,
        "slot": 2,
        "contrato_publicidade_id": 1,
    }


@pytest.fixture
def get_allocate_video_schedule_without_contract():
    return {
        "fan_id": 1,
        "video_id": 1,
        "slot": 1,
    }


@pytest.fixture
def get_allocate_video_schedule_with_multiples_contracts():
    return {
        "fan_id": 1,
        "video_id": 1,
        "slot": 1,
        "contrato_instalacao_id": 1,
        "contrato_publicidade_id": 1,
    }


@pytest.fixture
def get_duplicate_schedule_dict():
    return {"data": "2024-02-18"}


@pytest.fixture(scope="module")
def superuser_refresh_token(
    client: TestClient,
    get_fake_container,
    app,
):
    with app.container.user_service.override(
        get_fake_container.user_service
    ):
        return refresh_token_from_superuser(client=client)


@pytest.fixture(scope="module")
def superuser_tokens(
    client: TestClient,
    get_fake_container,
    app,
):
    with app.container.user_service.override(
        get_fake_container.user_service
    ):
        return authentication_token_from_superuser(
            client=client
        )


@pytest.fixture(scope="module")
def client(
    app: FastAPI,
) -> Generator[TestClient, Any, None]:
    os.environ["USING_TESTCLIENT"] = "true"
    """
    Create a new FastAPI TestClient that uses the `db_session` fixture to override
    the `get_db` dependency that is injected into routes.
    """

    with TestClient(app) as client:
        yield client
