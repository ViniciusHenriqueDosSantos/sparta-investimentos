# Sparta - API de Cálculo de Taxas de Fundos e Gestão de Portfólio

API REST para calcular taxas de administração de fundos de investimento e gerenciar portfólios de investimentos com movimentações de ações.

## ⚠️ Importante

**O endpoint original solicitado no teste (`/calculate-fees`) está implementado** Todas as funcionalidades adicionais (gestão de investidores, fundos, movimentações e cálculos avançados) são **extras**.

## Como Executar

### Opção 1: Script Automático
```bash
python run.py build    # Instala dependências, inicializa banco e inicia, RECOMENDADO
python run.py start    # Apenas inicia
python run.py init     # Inicializa apenas o banco de dados
```

### Opção 2: Manual
```bash
pip install -r requirements.txt
python init_database.py  # Inicializa banco com dados de exemplo
python -m uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```

## 📚 Documentação da API

**A API possui documentação completa e interativa via Swagger**

🔗 **Acesse a documentação**: <a href="http://localhost:8000/docs" target="_blank">http://localhost:8000/docs</a>


### Endpoints Disponíveis

A API inclui:

- **Endpoint Original**: `POST /calculate-fees` (conforme especificação do teste)
- **Gestão de Investidores**: Cadastro e listagem de investidores
- **Gestão de Ações/Fundos**: Cadastro e listagem de fundos Sparta
- **Movimentações**: Registro de operações de compra
- **Cálculos Avançados**: Taxas por data e por investidor específico


## Principais Decisões Técnicas

- **FastAPI**: Framework moderno com documentação automática
- **Arquitetura MVC**: Separação clara entre Models, Controllers e Services
- **Pydantic**: Validação automática de dados com type hints
- **SQLAlchemy**: ORM para interação com banco de dados
- **SQLite**: Banco de dados local para desenvolvimento e testes


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
Soube que a empresa está em processo de transição do Excel para um sistema completo. Uma funcionalidade muito útil seria a integração com arquivos Excel usando bibliotecas como `pandas` e `openpyxl`, esta funcionalidade tornaria o sistema ainda mais prático para os funcionária.