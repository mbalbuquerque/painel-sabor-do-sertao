# Painel de Análise de Dados - Sabor do Sertão

Atividade prática de análise de dados utilizando **Python, Streamlit, Pandas e Plotly**.

O projeto simula a análise das vendas da rede fictícia de lanchonetes **Sabor do Sertão**, com unidades em Recife, Olinda, Caruaru, Petrolina e Garanhuns.

## Objetivo

Desenvolver um painel interativo capaz de analisar:

- onde ocorrem mais vendas;
- quais produtos são mais vendidos;
- períodos com maior faturamento;
- formas de pagamento utilizadas pelos clientes.

## Funcionalidades

O painel possui:

- exploração inicial dos dados;
- tratamento de valores ausentes;
- faturamento total;
- número de vendas;
- ticket médio;
- avaliação média;
- filtro por cidade;
- filtro por categoria;
- filtro por período;
- faturamento mensal;
- faturamento por cidade;
- Top 5 produtos mais vendidos;
- análise das formas de pagamento;
- insights gerenciais;
- exportação dos dados filtrados em CSV;
- explorador livre de dados.

## Tecnologias utilizadas

- Python
- Streamlit
- Pandas
- Plotly
- NumPy

## Estrutura do projeto

```text
sabor-do-sertao/
├── app.py
├── gerar_dados.py
├── requirements.txt
├── README.md
└── vendas_sabor_do_sertao.csv
```

## Instalação

Instale as dependências:

```bash
pip install -r requirements.txt
```

## Gerar os dados

Execute:

```bash
python gerar_dados.py
```

O script gera o arquivo:

```text
vendas_sabor_do_sertao.csv
```

com 5.000 registros de vendas fictícias.

## Executar o painel

Execute:

```bash
python -m streamlit run app.py
```

Depois acesse no navegador:

```text
http://localhost:8501
```

## Painel

O painel apresenta indicadores e gráficos que respondem aos filtros selecionados pelo usuário.

### Visualização do painel

![Painel Sabor do Sertão](painel.png)

## Atividade

Projeto desenvolvido como atividade prática de **Painel de Análise de Dados com Streamlit**.

O objetivo é aplicar conceitos de manipulação, exploração e visualização de dados utilizando Python.