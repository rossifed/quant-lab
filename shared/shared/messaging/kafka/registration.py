from aiokafka import AIOKafkaProducer, AIOKafkaConsumer  # type: ignore
from shared.di.protocols import DIContainer
from shared.messaging.kafka.kafka_message_broker import KafkaMessageBroker
from shared.messaging.kafka.kafka_messaging_client import KafkaMessagingClient
from shared.messaging.kafka.kafka_message_consumer import KafkaMessageConsumer
from shared.messaging.kafka.kafka_settings import KafkaSettings
from typing import Any


def add_kafka_messaging(container: DIContainer, settings: KafkaSettings) -> None:
    producer_kwargs: dict[str, Any] = {
        "bootstrap_servers": settings.bootstrap_servers,
        "security_protocol": settings.security_protocol,
    }
    if settings.sasl_mechanism:
        producer_kwargs["sasl_mechanism"] = settings.sasl_mechanism
        producer_kwargs["sasl_plain_username"] = settings.username
        producer_kwargs["sasl_plain_password"] = settings.password

    container.add_singleton(
        AIOKafkaProducer,
        lambda: AIOKafkaProducer(**producer_kwargs)  # type: ignore[arg-type]
    )

    consumer_kwargs: dict[str, Any] = {
        "bootstrap_servers": settings.bootstrap_servers,
        "group_id": settings.group_id,
        "security_protocol": settings.security_protocol,
    }
    if settings.sasl_mechanism:
        consumer_kwargs["sasl_mechanism"] = settings.sasl_mechanism
        consumer_kwargs["sasl_plain_username"] = settings.username
        consumer_kwargs["sasl_plain_password"] = settings.password

    container.add_singleton(
        AIOKafkaConsumer,
        lambda: AIOKafkaConsumer(  # type: ignore[arg-type]
            settings.topic,
            **consumer_kwargs
        )
    )


    container.add_singleton(
        KafkaMessageBroker,
        lambda: KafkaMessageBroker(
            producer=container.resolve(AIOKafkaProducer)
        )
    )

    container.add_singleton(
        KafkaMessagingClient,
        lambda: KafkaMessagingClient(
            producer=container.resolve(AIOKafkaProducer),
            consumer=container.resolve(AIOKafkaConsumer)
        )
    )

    container.add_singleton(
        KafkaMessageConsumer,
        lambda: KafkaMessageConsumer(
            consumer=container.resolve(AIOKafkaConsumer)
        )
    )