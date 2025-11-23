from pydantic import BaseModel
from shared.logging import LoggingSettings
from shared.messaging.kafka import KafkaSettings


class Settings(BaseModel):
    app_name: str = "backtesting-service"
    
    # Logging
    log_level: str = "INFO"
    log_format: str = "%(asctime)s | %(levelname)s | %(name)s | %(message)s"
    
    # Kafka
    kafka_bootstrap_servers: str = "redpanda:9092"
    kafka_topic: str = "backtesting-events"
    kafka_group_id: str = "backtesting-group"
    kafka_security_protocol: str = "PLAINTEXT"
    
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
    
    def get_logging_settings(self) -> LoggingSettings:
        return LoggingSettings(
            app_name=self.app_name,
            level=self.log_level,  # type: ignore
            format=self.log_format
        )
    
    def get_kafka_settings(self) -> KafkaSettings:
        return KafkaSettings(
            bootstrap_servers=self.kafka_bootstrap_servers,
            topic=self.kafka_topic,
            group_id=self.kafka_group_id,
            security_protocol=self.kafka_security_protocol
        )
