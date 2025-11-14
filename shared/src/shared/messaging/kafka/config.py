from aiokafka import AIOKafkaProducer, AIOKafkaConsumer  # type: ignore
from shared.di.protocols import DIContainer
from shared.messaging.kafka.kafka_message_broker import KafkaMessageBroker
from shared.messaging.kafka.kafka_messaging_client import KafkaMessagingClient
from shared.messaging.kafka.kafka_settings import KafkaSettings


def configure_kafka_messaging(container: DIContainer, settings: KafkaSettings) -> None:

    container.add_singleton(
        AIOKafkaProducer,
        lambda: AIOKafkaProducer(
            bootstrap_servers=settings.bootstrap_servers,
            security_protocol=settings.security_protocol,
            sasl_mechanism=settings.sasl_mechanism,
            sasl_plain_username=settings.username,
            sasl_plain_password=settings.password,
        )
    )

    container.add_singleton(
        AIOKafkaConsumer,
        lambda: AIOKafkaConsumer(
            settings.topic,
            bootstrap_servers=settings.bootstrap_servers,
            group_id=settings.group_id,
            security_protocol=settings.security_protocol,
            sasl_mechanism=settings.sasl_mechanism,
            sasl_plain_username=settings.username,
            sasl_plain_password=settings.password,
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