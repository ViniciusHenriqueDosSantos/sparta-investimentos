from fastapi import HTTPException, Depends
from sqlalchemy.orm import Session
from typing import List
from database.database import get_db
from services.stock_service import StockService
from models.portfolio_models import StockCreate, StockResponse, StockListResponse

class StockController:
    
    def __init__(self):
        self.stock_service = StockService()
    
    async def create_stock(self, stock_data: StockCreate, db: Session) -> StockResponse:
        try:
            existing_stock = self.stock_service.get_stock_by_symbol(db, stock_data.symbol)
            if existing_stock:
                raise HTTPException(status_code=400, detail="Ação com este símbolo já existe")
            
            db_stock = self.stock_service.create_stock(db, stock_data)
            return StockResponse.model_validate(db_stock)
            
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Erro ao criar ação: {str(e)}")
    
    async def get_stocks(self, db: Session) -> StockListResponse:
        try:
            stocks = self.stock_service.get_stocks(db)
            total = self.stock_service.get_stocks_count(db)
            
            stock_responses = [StockResponse.model_validate(stock) for stock in stocks]
            
            return StockListResponse(
                stocks=stock_responses,
                total=total
            )
            
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Erro ao buscar ações: {str(e)}")
    
