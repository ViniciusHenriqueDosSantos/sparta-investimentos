from fastapi import HTTPException
from typing import List
from services.fee_calculation_service import FeeCalculationService
from models.fee_models import FeeCalculationRequest

class FeeController:
    """Controller para requisições de cálculo de taxa de administração"""
    
    def __init__(self):
        self.fee_service = FeeCalculationService()
    
    async def calculate_fees(self, request_data: dict) -> List[float]:
        """
        Processa requisição de cálculo
        
        Args:
            request_data: Dados da requisição
            
        Returns:
            Taxas calculadas
        """
        try:

            validated_request = FeeCalculationRequest(**request_data)
            

            taxa = validated_request.taxa
            cotas_data = [{"valor": cota.valor, "quantidades": cota.quantidades} for cota in validated_request.cotas]
            
            fees = self.fee_service.calculate_fees(taxa, cotas_data)
            
            return fees
            
        except ValueError as e:
            raise HTTPException(status_code=400, detail=str(e))
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Erro interno do servidor: {str(e)}")
