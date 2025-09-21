from fastapi import HTTPException, Depends
from sqlalchemy.orm import Session
from typing import List, Optional
from database.database import get_db
from services.portfolio_fee_service import PortfolioFeeService
from models.portfolio_models import (
    FeeCalculationByDateRequest, 
    FeeCalculationByInvestorRequest
)

class PortfolioFeeController:
    
    def __init__(self):
        self.portfolio_fee_service = PortfolioFeeService()
    
    async def calculate_fees_by_date(self, request: FeeCalculationByDateRequest, 
                                    db: Session) -> List[dict]:
        try:
            results = self.portfolio_fee_service.calculate_fees_by_date(db, request)
            return results
            
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Erro ao calcular taxas por data: {str(e)}")
    
    async def calculate_fees_by_investor(self, request: FeeCalculationByInvestorRequest,
                                    db: Session) -> dict:
        try:
            result = self.portfolio_fee_service.calculate_fees_by_investor(db, request)
            return result
            
        except ValueError as e:
            raise HTTPException(status_code=400, detail=str(e))
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Erro ao calcular taxas por investidor: {str(e)}")
    