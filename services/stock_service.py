from sqlalchemy.orm import Session
from typing import List, Optional
from database.models import Stock
from models.portfolio_models import StockCreate, StockResponse

class StockService:
    
    def create_stock(self, db: Session, stock_data: StockCreate) -> Stock:
        db_stock = Stock(
            symbol=stock_data.symbol,
            name=stock_data.name
        )
        db.add(db_stock)
        db.commit()
        db.refresh(db_stock)
        return db_stock
    
    def get_stock_by_symbol(self, db: Session, symbol: str) -> Optional[Stock]:
        return db.query(Stock).filter(Stock.symbol == symbol.upper()).first()
    
    def get_stocks(self, db: Session) -> List[Stock]:
        return db.query(Stock).all()
    
    def get_stocks_count(self, db: Session) -> int:
        return db.query(Stock).count()
    
