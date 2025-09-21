from sqlalchemy.orm import Session
from typing import List, Optional
from database.models import Investor
from models.portfolio_models import InvestorCreate, InvestorResponse

class InvestorService:
    
    def create_investor(self, db: Session, investor_data: InvestorCreate) -> Investor:
        db_investor = Investor(
            name=investor_data.name,
            email=investor_data.email
        )
        db.add(db_investor)
        db.commit()
        db.refresh(db_investor)
        return db_investor
    
    def get_investor(self, db: Session, investor_id: int) -> Optional[Investor]:
        return db.query(Investor).filter(Investor.id == investor_id).first()
    
    def get_investor_by_email(self, db: Session, email: str) -> Optional[Investor]:
        return db.query(Investor).filter(Investor.email == email).first()
    
    def get_investors(self, db: Session) -> List[Investor]:
        return db.query(Investor).all()
    
    def get_investors_count(self, db: Session) -> int:
        return db.query(Investor).count()
