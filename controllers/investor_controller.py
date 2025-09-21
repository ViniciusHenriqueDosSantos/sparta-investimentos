from fastapi import HTTPException, Depends
from sqlalchemy.orm import Session
from typing import List
from database.database import get_db
from services.investor_service import InvestorService
from models.portfolio_models import InvestorCreate, InvestorResponse, InvestorListResponse

class InvestorController:
    
    def __init__(self):
        self.investor_service = InvestorService()
    
    async def create_investor(self, investor_data: InvestorCreate, db: Session) -> InvestorResponse:
        try:
            existing_investor = self.investor_service.get_investor_by_email(db, investor_data.email)
            if existing_investor:
                raise HTTPException(status_code=400, detail="Investidor com este email já existe")
            
            db_investor = self.investor_service.create_investor(db, investor_data)
            return InvestorResponse.model_validate(db_investor)
            
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Erro ao criar investidor: {str(e)}")
    
    async def get_investor(self, investor_id: int, db: Session) -> InvestorResponse:
        try:
            db_investor = self.investor_service.get_investor(db, investor_id)
            if not db_investor:
                raise HTTPException(status_code=404, detail="Investidor não encontrado")
            
            return InvestorResponse.model_validate(db_investor)
            
        except HTTPException:
            raise
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Erro ao buscar investidor: {str(e)}")
    
    async def get_investors(self, db: Session) -> InvestorListResponse:
        try:
            investors = self.investor_service.get_investors(db)
            total = self.investor_service.get_investors_count(db)
            
            investor_responses = [InvestorResponse.model_validate(investor) for investor in investors]
            
            return InvestorListResponse(
                investors=investor_responses,
                total=total
            )
            
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Erro ao buscar investidores: {str(e)}")
