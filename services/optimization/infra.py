from fastapi import FastAPI
from shared.app_container import get_container
from shared.infra import load_shared_infrastructure
from services.optimization.config import configure_optimization

def load_service_infrastructure(app: FastAPI):
    """
    Charge l'infrastructure spécifique au service Optimization.
    """
    container = get_container()

    # Charger les dépendances partagées
    load_shared_infrastructure(container)

    # Charger les dépendances spécifiques au service Optimization
    configure_optimization(container)

    # Ajouter des gestionnaires d'événements FastAPI
    async def start_background_services():
        # Exemple : démarrer un service de fond si nécessaire
        pass

    async def stop_background_services():
        # Exemple : arrêter un service de fond si nécessaire
        pass

    app.add_event_handler("startup", start_background_services)
    app.add_event_handler("shutdown", stop_background_services)