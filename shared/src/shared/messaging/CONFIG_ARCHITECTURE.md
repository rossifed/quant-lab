# Messaging Configuration Architecture

## Registry Pattern - Auto-registration

Chaque backend de messaging (Kafka, Redis, RabbitMQ) **s'enregistre lui-même** au moment de l'import. Plus besoin de if/elif dégueulasses !

### Comment ça marche ?

#### 1. Le Registry (`messaging/config.py`)
```python
_BACKEND_REGISTRY: Dict[str, Callable] = {}

def register_messaging_backend(backend_name: str, loader: Callable):
    """Enregistre un backend."""
    _BACKEND_REGISTRY[backend_name] = loader

class MessagingConfig:
    def to_settings(self) -> MessagingSettings:
        # Pas de if/elif ! Juste un lookup dans le registry
        loader = _BACKEND_REGISTRY.get(self.backend)
        return loader(self.kafka)  # Le backend parse sa propre config
```

#### 2. Chaque backend s'enregistre (`kafka/kafka_settings.py`)
```python
class KafkaSettings(BaseModel):
    @classmethod
    def from_config(cls, config: dict) -> "KafkaSettings":
        return cls(**config)

# Auto-registration au moment de l'import !
register_messaging_backend("kafka", KafkaSettings.from_config)
```

#### 3. Import automatique (`messaging/__init__.py`)
```python
# Importe tous les backends pour déclencher leur auto-registration
from . import kafka  # Déclenche l'enregistrement de Kafka
```

### Ajouter un nouveau backend (Redis, RabbitMQ, etc.)

1. Créer `shared/messaging/redis/redis_settings.py` :
```python
class RedisSettings(BaseModel):
    host: str
    port: int
    
    def get_backend(self) -> str:
        return "redis"
    
    @classmethod
    def from_config(cls, config: dict) -> "RedisSettings":
        return cls(**config)

# Auto-registration
from shared.messaging.config import register_messaging_backend
register_messaging_backend("redis", RedisSettings.from_config)
```

2. Importer dans `messaging/__init__.py` :
```python
from . import kafka
from . import redis  # Nouveau !
```

3. C'est tout ! Pas besoin de modifier `config.py` ou d'ajouter des if/elif

### Config YAML
```yaml
messaging:
  backend: "redis"  # Change juste ça !
  redis:
    host: "localhost"
    port: 6379
```

Le service ne change pas, le registry trouve automatiquement le bon loader !

## Avantages

- ✅ **Pas de if/elif chains** : Lookup dans un dictionnaire
- ✅ **Open/Closed Principle** : Ajouter un backend sans modifier le code existant
- ✅ **Auto-discovery** : Les backends s'enregistrent eux-mêmes
- ✅ **Type-safe** : Chaque backend valide sa propre config
- ✅ **Découplage** : Le service ne connaît aucune implémentation concrète
