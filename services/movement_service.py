from sqlalchemy.orm import Session
from sqlalchemy import and_
from typing import List, Optional
from datetime import datetime
from database.models import Movement, Investor, Stock
from models.portfolio_models import MovementCreate, MovementResponse

class MovementService:
    
    def create_movement(self, db: Session, movement_data: MovementCreate) -> Movement:
        investor = db.query(Investor).filter(Investor.id == movement_data.investor_id).first()
        if not investor:
            raise ValueError(f"Investidor com ID {movement_data.investor_id} não encontrado")
        
        stock = db.query(Stock).filter(Stock.id == movement_data.stock_id).first()
        if not stock:
            raise ValueError(f"Ação com ID {movement_data.stock_id} não encontrada")
        
        db_movement = Movement(
            investor_id=movement_data.investor_id,
            stock_id=movement_data.stock_id,
            stock_value=movement_data.stock_value,
            date_of_occurrence=movement_data.date_of_occurrence
        )
        db.add(db_movement)
        db.commit()
        db.refresh(db_movement)
        return db_movement
    
    def get_movement(self, db: Session, movement_id: int) -> Optional[Movement]:
        return db.query(Movement).filter(Movement.id == movement_id).first()
    
    def get_movements(self, db: Session, investor_id: Optional[int] = None, stock_id: Optional[int] = None) -> List[Movement]:
        query = db.query(Movement)
        
        if investor_id:
            query = query.filter(Movement.investor_id == investor_id)
        if stock_id:
            query = query.filter(Movement.stock_id == stock_id)
        
        return query.order_by(Movement.date_of_occurrence.desc()).all()
    
    def get_movements_count(self, db: Session, investor_id: Optional[int] = None, 
                           stock_id: Optional[int] = None) -> int:
        query = db.query(Movement)
        
        if investor_id:
            query = query.filter(Movement.investor_id == investor_id)
        if stock_id:
            query = query.filter(Movement.stock_id == stock_id)
        
        return query.count()
    
    def get_movements_by_investor(self, db: Session, investor_id: int) -> List[Movement]:
        return self.get_movements(db, investor_id=investor_id)
    
    def get_movements_by_date_range(self, db: Session, start_date: datetime, 
                                   end_date: datetime, investor_id: Optional[int] = None) -> List[Movement]:
        query = db.query(Movement).filter(
            and_(
                Movement.date_of_occurrence >= start_date,
                Movement.date_of_occurrence <= end_date
            )
        )
        
        if investor_id:
            query = query.filter(Movement.investor_id == investor_id)
        
        return query.order_by(Movement.date_of_occurrence.desc()).all()
    
    def get_investor_portfolio_summary(self, db: Session, investor_id: int, as_of_date: datetime) -> dict:
        movements = self.get_movements_by_date_range(
            db, 
            datetime.min.replace(year=1900),
            as_of_date, 
            investor_id=investor_id
        )
        
        portfolio = {}
        for movement in movements:
            stock_symbol = movement.stock.symbol
            if stock_symbol not in portfolio:
                portfolio[stock_symbol] = {
                    'stock_id': movement.stock_id,
                    'stock_name': movement.stock.name,
                    'total_value': 0,
                    'movements_count': 0
                }
            
            portfolio[stock_symbol]['total_value'] += movement.stock_value
            portfolio[stock_symbol]['movements_count'] += 1
        
        return portfolio
