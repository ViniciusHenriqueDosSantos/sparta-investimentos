from fastapi import FastAPI, Depends
from typing import Optional
from controllers.fee_controller import FeeController
from controllers.investor_controller import InvestorController
from controllers.stock_controller import StockController
from controllers.movement_controller import MovementController
from controllers.portfolio_fee_controller import PortfolioFeeController
from models.fee_models import FeeCalculationRequest
from models.portfolio_models import (
    InvestorCreate, InvestorResponse, InvestorListResponse,
    StockCreate, StockResponse, StockListResponse,
    MovementCreate, MovementResponse, MovementListResponse,
    FeeCalculationByDateRequest, FeeCalculationByInvestorRequest
)
from database.database import create_tables, get_db
from sqlalchemy.orm import Session

app = FastAPI(
    title="Sparta - API de Gestão de Investimentos",
    description="API para cálculo de taxas de fundos de investimento e gestão de portfólios com movimentações em fundos Sparta",
    version="2.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

fee_controller = FeeController()
investor_controller = InvestorController()
stock_controller = StockController()
movement_controller = MovementController()
portfolio_fee_controller = PortfolioFeeController()


@app.get("/", 
         summary="Status da API", 
         description="Endpoint de verificação do status da API Sparta")
async def root():
    return {"message": "Sparta API - Vinicius"}

@app.post("/calculate-fees", 
          response_model=list[float],
          summary="Calcular Taxas de Fundos",
          description="Calcula taxas de administração de fundos de investimento (como pedido)")
async def calculate_fees(request_data: FeeCalculationRequest):
    return await fee_controller.calculate_fees(request_data.dict())

@app.post("/investors", 
          response_model=InvestorResponse,
          summary="Criar Investidor",
          description="Cria um novo investidor no sistema")
async def create_investor(investor_data: InvestorCreate, db: Session = Depends(get_db)):
    return await investor_controller.create_investor(investor_data, db)

@app.get("/investors", 
         response_model=InvestorListResponse,
         summary="Listar Investidores",
         description="Lista todos os investidores cadastrados no sistema")
async def get_investors(db: Session = Depends(get_db)):
    return await investor_controller.get_investors(db)

@app.get("/investors/{investor_id}", 
         response_model=InvestorResponse,
         summary="Buscar Investidor",
         description="Busca um investidor específico pelo ID")
async def get_investor(investor_id: int, db: Session = Depends(get_db)):
    return await investor_controller.get_investor(investor_id, db)

@app.post("/stocks", 
          response_model=StockResponse,
          summary="Adicionar Fundo",
          description="Adiciona um novo fundo Sparta ao sistema")
async def create_stock(stock_data: StockCreate, db: Session = Depends(get_db)):
    return await stock_controller.create_stock(stock_data, db)

@app.get("/stocks", 
         response_model=StockListResponse,
         summary="Listar Fundos",
         description="Lista todos os fundos Sparta disponíveis para investimento")
async def get_stocks(db: Session = Depends(get_db)):
    return await stock_controller.get_stocks(db)

@app.post("/movements", 
          response_model=MovementResponse,
          summary="Criar Movimentação",
          description="Registra uma nova movimentação de investimento em fundo")
async def create_movement(movement_data: MovementCreate, db: Session = Depends(get_db)):
    return await movement_controller.create_movement(movement_data, db)

@app.get("/movements", 
         response_model=MovementListResponse,
         summary="Listar Movimentações",
         description="Lista todas as movimentações com filtros opcionais por investidor e fundo")
async def get_movements(investor_id: Optional[int] = None, stock_id: Optional[int] = None, db: Session = Depends(get_db)):
    return await movement_controller.get_movements(db, investor_id, stock_id)

@app.get("/movements/{movement_id}", 
         response_model=MovementResponse,
         summary="Buscar Movimentação",
         description="Busca uma movimentação específica pelo ID")
async def get_movement(movement_id: int, db: Session = Depends(get_db)):
    return await movement_controller.get_movement(movement_id, db)

@app.get("/movements/investor/{investor_id}", 
         response_model=MovementListResponse,
         summary="Movimentações do Investidor",
         description="Lista todas as movimentações de um investidor específico")
async def get_movements_by_investor(investor_id: int, db: Session = Depends(get_db)):
    return await movement_controller.get_movements_by_investor(investor_id, db)

@app.get("/investors/{investor_id}/portfolio",
         summary="Portfólio do Investidor",
         description="Obtém o resumo do portfólio de um investidor em uma data específica")
async def get_investor_portfolio(investor_id: int, as_of_date: str, db: Session = Depends(get_db)):
    from datetime import datetime
    as_of_date_dt = datetime.fromisoformat(as_of_date.replace('Z', '+00:00'))
    return await movement_controller.get_investor_portfolio_summary(investor_id, as_of_date_dt, db)

@app.post("/calculate-fees/by-date",
          summary="Calcular Taxas por Data",
          description="Calcula taxas de administração para todos os investidores em uma data específica")
async def calculate_fees_by_date(request: FeeCalculationByDateRequest, db: Session = Depends(get_db)):
    return await portfolio_fee_controller.calculate_fees_by_date(request, db)

@app.post("/calculate-fees/by-investor",
          summary="Calcular Taxas por Investidor",
          description="Calcula taxas de administração para um investidor específico em uma data")
async def calculate_fees_by_investor(request: FeeCalculationByInvestorRequest, db: Session = Depends(get_db)):
    return await portfolio_fee_controller.calculate_fees_by_investor(request, db)
