from fastapi import HTTPException, Depends
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import datetime
from database.database import get_db
from services.movement_service import MovementService
from models.portfolio_models import MovementCreate, MovementResponse, MovementListResponse

class MovementController:
    
    def __init__(self):
        self.movement_service = MovementService()
    
    async def create_movement(self, movement_data: MovementCreate, db: Session) -> MovementResponse:
        try:
            db_movement = self.movement_service.create_movement(db, movement_data)
            return MovementResponse.model_validate(db_movement)
            
        except ValueError as e:
            raise HTTPException(status_code=400, detail=str(e))
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Erro ao criar movimento: {str(e)}")
    
    async def get_movement(self, movement_id: int, db: Session) -> MovementResponse:
        try:
            db_movement = self.movement_service.get_movement(db, movement_id)
            if not db_movement:
                raise HTTPException(status_code=404, detail="Movimento não encontrado")
            
            return MovementResponse.model_validate(db_movement)
            
        except HTTPException:
            raise
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Erro ao buscar movimento: {str(e)}")
    
    async def get_movements(self, db: Session, investor_id: Optional[int] = None, stock_id: Optional[int] = None) -> MovementListResponse:
        try:
            movements = self.movement_service.get_movements(db, investor_id, stock_id)
            total = self.movement_service.get_movements_count(db, investor_id, stock_id)
            
            movement_responses = [MovementResponse.model_validate(movement) for movement in movements]
            
            return MovementListResponse(
                movements=movement_responses,
                total=total
            )
            
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Erro ao buscar movimentos: {str(e)}")
    
    async def get_movements_by_investor(self, investor_id: int, db: Session) -> MovementListResponse:
        try:
            movements = self.movement_service.get_movements_by_investor(db, investor_id)
            total = self.movement_service.get_movements_count(db, investor_id=investor_id)
            
            movement_responses = [MovementResponse.model_validate(movement) for movement in movements]
            
            return MovementListResponse(
                movements=movement_responses,
                total=total
            )
            
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Erro ao buscar movimentos do investidor: {str(e)}")
    
    async def get_investor_portfolio_summary(self, investor_id: int, db: Session) -> dict:
        try:
            portfolio = self.movement_service.get_investor_portfolio_summary(db, investor_id)
            return {
                "investor_id": investor_id,
                "portfolio": portfolio,
                "total_stocks": len(portfolio),
                "total_value": sum(stock['total_value'] for stock in portfolio.values())
            }
            
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Erro ao buscar resumo do portfólio: {str(e)}")