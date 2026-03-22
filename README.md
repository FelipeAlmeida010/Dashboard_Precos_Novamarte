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








# Dashboard_Precos_Novamarte



Requisitos

Antes de começar, você precisa ter instalado na máquina:

Python 3.x
Git
Como baixar o projeto do GitHub

Clone o repositório com o comando:

git clone https://github.com/FelipeAlmeida010/Dashboard_Precos_Novamarte.git

Depois entre na pasta do projeto:

cd Dashboard_Precos_Novamarte
Como criar o ambiente virtual

No terminal, execute:

py -m venv venv
Como ativar o ambiente virtual


Git Bash / Bash
source venv/Scripts/activate


PowerShell
venv\Scripts\Activate.ps1


Prompt de Comando (CMD)
venv\Scripts\activate

Quando o ambiente estiver ativo, o terminal deverá mostrar algo parecido com:

(venv)
Como instalar as dependências

Com o ambiente virtual ativado, rode:

pip install -r requirements.txt
Como rodar o projeto

Com o ambiente virtual ativado, execute:

streamlit run app.py

Depois disso, o Streamlit abrirá no navegador automaticamente.

Se isso não acontecer, o terminal mostrará uma URL local semelhante a esta:

http://localhost:8501
Como carregar os dados

O dashboard aceita duas formas de carregamento da base:

1. Upload pelo navegador

Você pode enviar diretamente um arquivo .csv ou .xlsx pela interface do app.

2. Arquivo salvo na pasta data/

Também é possível colocar o arquivo dentro da pasta data/ e selecioná-lo na aplicação.

Formato esperado da planilha

A base de dados deve conter as seguintes colunas:

Date
Customer_ID
Transaction_ID
SKU_Category
SKU
Quantity
Sales_Amount
Observações Importantes
O projeto trata arquivos .csv e .xlsx
Arquivos .csv com separador ; também são aceitos
Os filtros laterais ajudam na exploração dos dados por diferentes recortes
Este dashboard foi construído como apoio à análise comercial e visualização de desempenho operacional
Possíveis Evoluções do Projeto

Algumas melhorias futuras que podem ser incorporadas:

comparação entre períodos
gráficos mais avançados
análise de desempenho por cliente
indicadores por SKU com maior detalhamento
inclusão de dados de preço para análise de sensibilidade e elasticidade
deploy em nuvem para compartilhamento do dashboard
Autor

Desenvolvido por Felipe Almeida.

GitHub:

https://github.com/FelipeAlmeida010
Licença

Este projeto foi desenvolvido para fins de estudo, portfólio e apresentação de case.
