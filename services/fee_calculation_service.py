from typing import List

class FeeCalculationService:
    """Calculo para taxas de fundo"""
    
    def calculate_fees(self, taxa: float, cotas: List[dict]) -> List[float]:
        """
        Calcula taxas de fundo
        
        Args:
            taxa: Taxa anual (ex: 0.01 = 1%)
            cotas: Lista de dados com valor e quantidades
            
        Returns:
        """
        if not cotas:
            raise ValueError("Pelo menos uma cota é necessária")
        
        num_investidores = len(cotas[0]['quantidades'])
        for i, cota in enumerate(cotas):
            if len(cota['quantidades']) != num_investidores:
                raise ValueError(f"Cota {i}: {len(cota['quantidades'])} investidores, esperado {num_investidores}")
        
        taxas_investidores = [0.0] * num_investidores
        
        for cota in cotas:
            valor = cota['valor']
            quantidades = cota['quantidades']
            
            for i, quantidade in enumerate(quantidades):
                taxa_diaria = quantidade * valor * taxa
                taxas_investidores[i] += taxa_diaria
        
        return [round(taxa / 252, 4) for taxa in taxas_investidores]
