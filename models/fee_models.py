from pydantic import BaseModel, Field, field_validator
from typing import List

class CotaData(BaseModel):
    valor: float = Field(..., gt=0, description="Valor unitário da cota do fundo")
    quantidades: List[float] = Field(..., min_length=1, description="Quantidades de cotas por investidor")
    
    @field_validator('quantidades')
    @classmethod
    def validar_quantidades(cls, v):
        """Valida quantidades"""
        if not all(q >= 0 for q in v):
            raise ValueError("Quantidades devem ser positivas")
        return v
    
    class Config:
        json_schema_extra = {
            "example": {
                "valor": 100.0,
                "quantidades": [10, 20, 30]
            }
        }

class FeeCalculationRequest(BaseModel):
    taxa: float = Field(..., ge=0, description="Taxa de administração anual (>= 0.0)")
    cotas: List[CotaData] = Field(..., min_length=1, description="Dados das cotas do fundo por período")
    
    @field_validator('cotas')
    @classmethod
    def validar_investidores_consistentes(cls, v):
        """Valida consistência de investidores"""
        if len(v) > 1:
            quantidade_primeiro_dia = len(v[0].quantidades)
            for i, cota in enumerate(v[1:], 1):
                if len(cota.quantidades) != quantidade_primeiro_dia:
                    raise ValueError(f"Cota {i}: {len(cota.quantidades)} investidores, esperado {quantidade_primeiro_dia}")
        return v
    
    class Config:
        json_schema_extra = {
            "example": {
                "taxa": 0.01,
                "cotas": [
                    {
                        "valor": 100.0,
                        "quantidades": [10, 20, 30]
                    },
                    {
                        "valor": 101.5,
                        "quantidades": [10, 25, 30]
                    }
                ]
            }
        }

class FeeCalculationResponse(BaseModel):
    fees: List[float] = Field(..., description="Taxas de administração calculadas por investidor")
