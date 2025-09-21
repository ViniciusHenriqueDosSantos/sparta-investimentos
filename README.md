# Sparta - API de Cálculo de Taxas de Fundos e Gestão de Portfólio

API REST para calcular taxas de administração de fundos de investimento e gerenciar portfólios de investimentos com movimentações de ações.

## ⚠️ Importante

**O endpoint original solicitado no teste (`/calculate-fees`) está implementado** Todas as funcionalidades adicionais (gestão de investidores, fundos, movimentações e cálculos avançados) são **extras**.

## Como Executar

### Opção 1: Script Automático
```bash
python run.py build    # Instala dependências, inicializa banco e inicia
python run.py start    # Apenas inicia
python run.py init     # Inicializa apenas o banco de dados
```

### Opção 2: Manual
```bash
pip install -r requirements.txt
python init_database.py  # Inicializa banco com dados de exemplo
uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```

**Acesse**: http://localhost:8000/docs (documentação feita com swagger, pode ser usada para testes)

## Rotas Disponíveis

### Endpoints Originais (Requisitos do Teste Técnico)

#### GET /
- **Descrição**: Endpoint de health check
- **Resposta**: `{"message": "Sparta API - Vinicius"}`

#### POST /calculate-fees
- **Descrição**: Calcula taxas de administração do fundo (endpoint original)
- **Body**:
  ```json
  {
    "taxa": 0.01,
    "cotas": [
      {"valor": 100.0, "quantidades": [10, 20, 30]},
      {"valor": 101.5, "quantidades": [10, 25, 30]}
    ]
  }
  ```
- **Resposta**: `[0.08, 0.1801, 0.2399]`

### Endpoints Extras de Gestão de Investidores 

#### POST /investors
- **Descrição**: Criar novo investidor
- **Body**: `{"name": "João Silva", "email": "joao@email.com"}`

#### GET /investors
- **Descrição**: Listar investidores

#### GET /investors/{investor_id}
- **Descrição**: Buscar investidor por ID

### Endpoints de Gestão de Ações

#### POST /stocks
- **Descrição**: Adicionar nova ação
- **Body**: `{"symbol": "AAPL", "name": "Apple Inc."}`

#### GET /stocks
- **Descrição**: Listar ações disponíveis

### Endpoints de Movimentações

#### POST /movements
- **Descrição**: Criar nova movimentação
- **Body**: 
  ```json
  {
    "investor_id": 1,
    "stock_id": 2,
    "stock_value": 25.50,
    "date_of_occurrence": "2024-01-15T10:30:00"
  }
  ```

#### GET /movements
- **Descrição**: Listar movimentações (com filtros opcionais)

#### GET /movements/investor/{investor_id}
- **Descrição**: Listar movimentações de um investidor

#### GET /investors/{investor_id}/portfolio
- **Descrição**: Resumo do portfólio do investidor em uma data

### Endpoints de Cálculo de Taxas Avançado

#### POST /calculate-fees/by-date
- **Descrição**: Calcular taxas para todos os investidores em uma data
- **Body**: `{"calculation_date": "2024-01-31T00:00:00", "taxa": 0.01}`

#### POST /calculate-fees/by-investor
- **Descrição**: Calcular taxas para um investidor específico
- **Body**: `{"investor_id": 1, "calculation_date": "2024-01-31T00:00:00", "taxa": 0.01}`


## Principais Decisões Técnicas

- **FastAPI**: Framework moderno com documentação automática
- **Arquitetura MVC**: Separação clara entre Models, Controllers e Services
- **Pydantic**: Validação automática de dados com type hints
- **SQLAlchemy**: ORM para interação com banco de dados
- **SQLite**: Banco de dados local para desenvolvimento e testes
- **Alembic**: Migrações de banco de dados (preparado para uso futuro)

## Estrutura

```
├── main.py                    # Aplicação FastAPI principal
├── models/                    # Modelos Pydantic para validação
├── database/                  # Configuração e modelos do banco de dados
├── services/                  # Camada de lógica de negócio
├── controllers/               # Camada de controladores HTTP
├── init_database.py          # Script de inicialização do banco
└── run.py                    # Script de desenvolvimento
```

## Banco de Dados

O sistema utiliza SQLite com as seguintes tabelas:
- **investors**: Investidores do sistema
- **stocks**: Fundos Sparta disponíveis (JURO11, CDII11, CRAA11, DIVS11)
- **movements**: Movimentações de investidores

Para inicializar com dados de exemplo:
```bash
python run.py init
```

## Sugestões de Melhorias

Este projeto foi desenvolvido seguindo os requisitos do teste técnico, mas também inclui funcionalidades extras para demonstrar capacidade de expansão do sistema.

### Separação de Responsabilidades
- **Endpoint Original**: Mantive o endpoint `/calculate-fees` exatamente como solicitado no teste
- **Funcionalidades Extras**: Implementei um sistema de gestão de portfólio com investidores, fundos e movimentações

### Integração com Fundos Reais da Sparta
Tive o cuidado de utilizar os fundos reais da empresa Sparta no sistema:
- **JURO11**: Sparta Inf FIC FIII RF CP RL
- **CDII11**: Sparta Infra CDI FIC de FI em Infraestrutura RF
- **CRAA11**: Sparta Fiagro
- **DIVS11**: Sparta Infra Inflacao Longa FIC de FI em Infraestrutura RF RL

### Sugestão: Integração com Excel
Soube que a empresa está em processo de transição do Excel para um sistema completo. Uma funcionalidade muito útil seria a integração com arquivos Excel usando bibliotecas como `pandas` e `openpyxl`, esta funcionalidade tornaria o sistema ainda mais prático e alinhado com as necessidades reais da empresa.