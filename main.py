from fastapi import FastAPI
from controllers.fee_controller import FeeController
from models.fee_models import FeeCalculationRequest

app = FastAPI(
    title="Sparta API",
    description="Calcula taxas de fundos",
    version="1.0"
)

fee_controller = FeeController()

@app.get("/")
async def root():
    """Home"""
    return {"message": "Sparta API - Vinicius"}

@app.post("/calculate-fees", response_model=list[float])
async def calculate_fees(request_data: FeeCalculationRequest):
    """
    Calcula taxas de fundo
    
    - **taxa**: Taxa anual (0.01 = 1%)
    - **cotas**: Dados diários com valor e quantidades
    
    Retorna taxas para cada cotista
    """
    return await fee_controller.calculate_fees(request_data.dict())
