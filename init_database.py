import sys
import os
from datetime import datetime, timedelta

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from database.database import SessionLocal, create_tables
from database.models import Investor, Stock, Movement
from sqlalchemy.orm import Session

def init_sample_data():
    create_tables()
    
    db = SessionLocal()
    
    try:
        if db.query(Investor).first():
            print("Dados de exemplo já existem. Pulando inicialização.")
            return
        
        print("Inicializando banco de dados com dados de exemplo...")
        
        investors_data = [
            {"name": "João Silva", "email": "joao@email.com"},
            {"name": "Maria Santos", "email": "maria@email.com"},
            {"name": "Pedro Oliveira", "email": "pedro@email.com"},
            {"name": "Ana Costa", "email": "ana@email.com"},
        ]
        
        investors = []
        for investor_data in investors_data:
            investor = Investor(**investor_data)
            db.add(investor)
            investors.append(investor)
        
        db.commit()
        
        for investor in investors:
            db.refresh(investor)
        
        stocks_data = [
            {"symbol": "JURO11", "name": "Sparta Inf FIC FIII RF CP RL"},
            {"symbol": "CDII11", "name": "Sparta Infra CDI FIC de FI em Infraestrutura RF"},
            {"symbol": "CRAA11", "name": "Sparta Fiagro (Nome Oficial não disponível)"},
            {"symbol": "DIVS11", "name": "Sparta Infra Inflacao Longa FIC de FI em Infraestrutura RF RL"},
        ]
        
        stocks = []
        for stock_data in stocks_data:
            stock = Stock(**stock_data)
            db.add(stock)
            stocks.append(stock)
        
        db.commit()
        
        for stock in stocks:
            db.refresh(stock)
        
        movements_data = [
            {"investor_id": investors[0].id, "stock_id": stocks[0].id, "stock_value": 150.00, "date_of_occurrence": datetime.now() - timedelta(days=30)},
            {"investor_id": investors[0].id, "stock_id": stocks[1].id, "stock_value": 125.50, "date_of_occurrence": datetime.now() - timedelta(days=25)},
            {"investor_id": investors[0].id, "stock_id": stocks[0].id, "stock_value": 155.00, "date_of_occurrence": datetime.now() - timedelta(days=20)},
            
            {"investor_id": investors[1].id, "stock_id": stocks[1].id, "stock_value": 126.00, "date_of_occurrence": datetime.now() - timedelta(days=28)},
            {"investor_id": investors[1].id, "stock_id": stocks[2].id, "stock_value": 95.75, "date_of_occurrence": datetime.now() - timedelta(days=22)},
            {"investor_id": investors[1].id, "stock_id": stocks[3].id, "stock_value": 88.30, "date_of_occurrence": datetime.now() - timedelta(days=15)},
            
            {"investor_id": investors[2].id, "stock_id": stocks[0].id, "stock_value": 152.80, "date_of_occurrence": datetime.now() - timedelta(days=35)},
            {"investor_id": investors[2].id, "stock_id": stocks[2].id, "stock_value": 98.45, "date_of_occurrence": datetime.now() - timedelta(days=18)},
            
            {"investor_id": investors[3].id, "stock_id": stocks[3].id, "stock_value": 92.10, "date_of_occurrence": datetime.now() - timedelta(days=32)},
            {"investor_id": investors[3].id, "stock_id": stocks[1].id, "stock_value": 125.20, "date_of_occurrence": datetime.now() - timedelta(days=12)},
            {"investor_id": investors[3].id, "stock_id": stocks[3].id, "stock_value": 93.50, "date_of_occurrence": datetime.now() - timedelta(days=5)},
        ]
        
        for movement_data in movements_data:
            movement = Movement(**movement_data)
            db.add(movement)
        
        db.commit()
        
        print("Dados de exemplo criados com sucesso!")
        print(f"   - {len(investors)} investidores")
        print(f"   - {len(stocks)} fundos Sparta")
        print(f"   - {len(movements_data)} movimentações")
        
    except Exception as e:
        print(f"Erro ao inicializar banco de dados: {e}")
        db.rollback()
        raise
    finally:
        db.close()

if __name__ == "__main__":
    init_sample_data()
