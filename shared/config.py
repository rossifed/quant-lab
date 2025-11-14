import yaml
from shared.di.protocols import DIContainer
from shared.messaging.config import configure_messaging
from shared.logging.config import configure_logging
from shared.middleware.config import register_middleware
from fastapi import FastAPI
from pydantic import BaseModel
from shared.messaging.kafka.kafka_settings import KafkaSettings
def configure_infrastructure(app: FastAPI,container: DIContainer) -> None:
    # raw_config = load_config("config.yml")
    # app_config = map_settings(raw_config)


    kafka_settings = KafkaSettings(
    bootstrap_servers="localhost:9092",
    topic="example-topic",
    group_id="example-group",
    security_protocol="PLAINTEXT",
    sasl_mechanism=None,
    username=None,
    password=None
)
    # Configurer la messagerie (Kafka, etc.)
    configure_messaging(container, kafka_settings)

    # Configurer le logging
    configure_logging(container)

    register_middleware(app,container)


def load_config(file_path: str) -> dict:
    with open(file_path, "r") as file:
        return yaml.safe_load(file)   
    


class AppConfig(BaseModel):
    messaging: dict
    logging: dict
    middleware: dict

def map_settings(config: dict) -> AppConfig:
    return AppConfig(**config)