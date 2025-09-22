from sqlalchemy.orm import Session
from typing import List, Dict, Optional
from datetime import datetime
from database.models import Movement, Investor, Stock
from models.portfolio_models import FeeCalculationByDateRequest, FeeCalculationByInvestorRequest

class PortfolioFeeService:
    
    def calculate_fees_by_date(self, db: Session, request: FeeCalculationByDateRequest) -> List[Dict]:
        movements = db.query(Movement).filter(
            Movement.date_of_occurrence <= request.calculation_date
        ).all()
        
        investor_movements = {}
        for movement in movements:
            if movement.investor_id not in investor_movements:
                investor_movements[movement.investor_id] = []
            investor_movements[movement.investor_id].append(movement)
        
        results = []
        
        for investor_id, investor_movs in investor_movements.items():
            investor_fee = self._calculate_investor_fee(investor_movs, request.taxa)
            investor_fee['investor_id'] = investor_id
            investor_fee['investor_name'] = investor_movs[0].investor.name
            results.append(investor_fee)
        
        return results
    
    def calculate_fees_by_investor(self, db: Session, request: FeeCalculationByInvestorRequest) -> Dict:
        movements = db.query(Movement).filter(
            Movement.investor_id == request.investor_id
        ).all()
        
        if not movements:
            raise ValueError(f"Nenhum movimento encontrado para o investidor {request.investor_id}")
        
        investor_fee = self._calculate_investor_fee(movements, request.taxa)
        investor_fee['investor_id'] = request.investor_id
        investor_fee['investor_name'] = movements[0].investor.name
        
        return investor_fee
    
    def _calculate_investor_fee(self, movements: List[Movement], taxa: float) -> Dict:
        stock_values = {}
        
        for movement in movements:
            stock_symbol = movement.stock.symbol
            if stock_symbol not in stock_values:
                stock_values[stock_symbol] = {
                    'stock_name': movement.stock.name,
                    'total_value': 0,
                    'movements_count': 0
                }
            
            stock_values[stock_symbol]['total_value'] += movement.stock_value
            stock_values[stock_symbol]['movements_count'] += 1
        
        total_portfolio_value = sum(stock['total_value'] for stock in stock_values.values())
        total_fees = total_portfolio_value * taxa / 252
        
        return {
            'calculation_date': movements[-1].date_of_occurrence if movements else None,
            'taxa': taxa,
            'total_portfolio_value': round(total_portfolio_value, 2),
            'total_fees': float(f"{total_fees:.4f}"),
            'movements_count': len(movements),
            'stocks_count': len(stock_values),
            'stock_breakdown': stock_values
        }
    
    
