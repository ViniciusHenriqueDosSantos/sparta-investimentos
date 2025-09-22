from pydantic import BaseModel, Field, field_validator
from typing import List, Optional
from datetime import datetime
from decimal import Decimal

class InvestorCreate(BaseModel):
    name: str = Field(..., min_length=1, max_length=100, description="Nome completo do investidor")
    email: str = Field(..., description="Endereço de email do investidor")
    
    @field_validator('email')
    @classmethod
    def validate_email(cls, v):
        if '@' not in v:
            raise ValueError('Formato de email inválido')
        return v.lower()

class InvestorResponse(BaseModel):
    id: int
    name: str
    email: str
    created_at: datetime
    
    class Config:
        from_attributes = True

class StockCreate(BaseModel):
    symbol: str = Field(..., min_length=1, max_length=20, description="Símbolo do fundo (ex: JURO11, CDII11)")
    name: str = Field(..., min_length=1, max_length=200, description="Nome completo do fundo de investimento")
    
    @field_validator('symbol')
    @classmethod
    def validate_symbol(cls, v):
        return v.upper()

class StockResponse(BaseModel):
    id: int
    symbol: str
    name: str
    created_at: datetime
    
    class Config:
        from_attributes = True

class MovementCreate(BaseModel):
    investor_id: int = Field(..., description="ID do investidor que realizou a movimentação")
    stock_id: int = Field(..., description="ID do fundo de investimento")
    stock_value: float = Field(..., gt=0, description="Valor do fundo no momento da movimentação")
    date_of_occurrence: datetime = Field(..., description="Data e hora quando a movimentação ocorreu")
    
    @field_validator('stock_value')
    @classmethod
    def validate_stock_value(cls, v):
        if v <= 0:
            raise ValueError('Valor da ação deve ser positivo')
        return round(v, 2)

class MovementResponse(BaseModel):
    id: int
    investor_id: int
    stock_id: int
    stock_value: float
    date_of_occurrence: datetime
    created_at: datetime
    investor: Optional[InvestorResponse] = None
    stock: Optional[StockResponse] = None
    
    class Config:
        from_attributes = True

class FeeCalculationByDateRequest(BaseModel):
    calculation_date: datetime = Field(..., description="Data para o cálculo das taxas de administração")
    taxa: float = Field(..., ge=0, description="Taxa de administração anual (>= 0.0)")
    
    @field_validator('taxa')
    @classmethod
    def validate_taxa(cls, v):
        if v < 0:
            raise ValueError('Taxa deve ser não negativa')
        return v

class FeeCalculationByInvestorRequest(BaseModel):
    investor_id: int = Field(..., description="ID do investidor para o cálculo")
    taxa: float = Field(..., ge=0, description="Taxa de administração anual (>= 0.0)")
    
    @field_validator('taxa')
    @classmethod
    def validate_taxa(cls, v):
        if v < 0:
            raise ValueError('Taxa deve ser não negativa')
        return v


class InvestorListResponse(BaseModel):
    investors: List[InvestorResponse]
    total: int

class StockListResponse(BaseModel):
    stocks: List[StockResponse]
    total: int

class MovementListResponse(BaseModel):
    movements: List[MovementResponse]
    total: int
