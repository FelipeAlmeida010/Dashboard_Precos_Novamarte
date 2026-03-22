# Dashboard de Precos - NovaMart

Dashboard interativo desenvolvido em **Python + Streamlit** para análise de vendas, categorias, SKUs e comportamento transacional da operação comercial da **NovaMart**.

O projeto foi criado com foco em transformar dados transacionais em visualizações e indicadores que apoiem decisões comerciais de forma prática e objetiva.

---

## Visão Geral

Este dashboard permite explorar dados de vendas a partir de arquivos **`.csv`** ou **`.xlsx`**, oferecendo uma interface simples para acompanhamento de indicadores e análise por período, categoria e SKU.

A proposta é servir como base para um case de análise comercial, ajudando a identificar padrões de venda, desempenho por categoria e comportamento dos produtos ao longo do tempo.

---

## Funcionalidades

- Upload de arquivos `.csv` e `.xlsx`
- Leitura de arquivos salvos na pasta `data/`
- Filtros laterais por:
  - período
  - categoria
  - SKU
- Indicadores principais:
  - faturamento total
  - quantidade vendida
  - ticket médio
  - total de transações
  - clientes únicos
  - categorias
  - SKUs
- Visualizações gráficas para análise temporal e por categoria
- Resumo consolidado por categoria

---

## Tecnologias Utilizadas

- **Python**
- **Streamlit**
- **Pandas**
- **OpenPyXL**

---

## Estrutura do Projeto

```bash
Dashboard_Precos_Novamarte/
│
├── app.py
├── requirements.txt
├── README.md
├── .gitignore
└── data/








