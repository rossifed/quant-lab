from fastapi import FastAPI
from services.optimization.infra import load_service_infrastructure

app = FastAPI()

# Charger l'infrastructure spécifique au service
load_service_infrastructure(app)

@app.get("/")
async def root():
    return {"message": "Optimization service is running"}