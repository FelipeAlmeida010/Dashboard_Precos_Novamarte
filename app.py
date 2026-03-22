import streamlit as st
import pandas as pd
from pathlib import Path

st.set_page_config(page_title="Dashboard NovaMart", layout="wide")

st.title("Dashboard NovaMart")
st.write("Análise de vendas por período, categoria, SKU e comportamento transacional.")

def carregar_arquivo(arquivo):
    nome_arquivo = arquivo.name.lower()

    if nome_arquivo.endswith(".xlsx"):
        return pd.read_excel(arquivo)

    if nome_arquivo.endswith(".csv"):
        try:
            return pd.read_csv(arquivo)
        except Exception:
            arquivo.seek(0)
            return pd.read_csv(arquivo, sep=";")

    raise ValueError("Formato de arquivo não suportado. Use .csv ou .xlsx")


st.subheader("Origem dos Dados")
origem = st.radio(
    "Escolha como deseja carregar a planilha:",
    ["Upload pelo navegador", "Arquivo da pasta data"]
)

df = None

if origem == "Upload pelo navegador":
    uploaded_file = st.file_uploader("Envie sua planilha", type=["csv", "xlsx"])

    if uploaded_file is not None:
        try:
            df = carregar_arquivo(uploaded_file)
            st.success(f"Arquivo carregado com sucesso: {uploaded_file.name}")
        except Exception as e:
            st.error(f"Erro ao ler o arquivo: {e}")

elif origem == "Arquivo da pasta data":
    pasta_data = Path("data")
    pasta_data.mkdir(exist_ok=True)

    arquivos_disponiveis = list(pasta_data.glob("*.csv")) + list(pasta_data.glob("*.xlsx"))

    if arquivos_disponiveis:
        arquivo_selecionado = st.selectbox(
            "Selecione um arquivo da pasta data:",
            arquivos_disponiveis,
            format_func=lambda x: x.name
        )

        if arquivo_selecionado is not None:
            try:
                df = carregar_arquivo(arquivo_selecionado)
                st.success(f"Arquivo carregado com sucesso: {arquivo_selecionado.name}")
            except Exception as e:
                st.error(f"Erro ao ler o arquivo: {e}")
    else:
        st.warning("Nenhum arquivo .csv ou .xlsx encontrado na pasta data/")

if df is not None:
    try:
        colunas_esperadas = [
            "Date",
            "Customer_ID",
            "Transaction_ID",
            "SKU_Category",
            "SKU",
            "Quantity",
            "Sales_Amount"
        ]

        colunas_faltando = [col for col in colunas_esperadas if col not in df.columns]

        if colunas_faltando:
            st.error(f"Colunas obrigatórias não encontradas: {colunas_faltando}")
            st.stop()

        # Tratamento básico
        df["Date"] = pd.to_datetime(df["Date"], errors="coerce")
        df["Quantity"] = pd.to_numeric(df["Quantity"], errors="coerce")
        df["Sales_Amount"] = pd.to_numeric(df["Sales_Amount"], errors="coerce")
        df["SKU_Category"] = df["SKU_Category"].astype(str)
        df["SKU"] = df["SKU"].astype(str)
        df["Customer_ID"] = df["Customer_ID"].astype(str)
        df["Transaction_ID"] = df["Transaction_ID"].astype(str)

        df = df.dropna(subset=["Date", "Quantity", "Sales_Amount"])

        # =========================
        # FILTROS NA SIDEBAR
        # =========================
        st.sidebar.header("Filtros")

        data_min = df["Date"].min().date()
        data_max = df["Date"].max().date()

        st.sidebar.subheader("Período")
        intervalo_datas = st.sidebar.date_input(
            "Selecione o período",
            value=(data_min, data_max),
            min_value=data_min,
            max_value=data_max
        )

        categorias = sorted(df["SKU_Category"].dropna().astype(str).unique().tolist())
        st.sidebar.subheader("Categoria")
        categorias_selecionadas = st.sidebar.multiselect(
            "Selecione as categorias",
            options=categorias,
            default=categorias
        )

        skus = sorted(df["SKU"].dropna().astype(str).unique().tolist())
        st.sidebar.subheader("SKU")
        skus_selecionados = st.sidebar.multiselect(
            "Selecione os SKUs",
            options=skus,
            default=skus
        )

        if st.sidebar.button("Limpar filtros"):
            st.rerun()

        # =========================
        # APLICAÇÃO DOS FILTROS
        # =========================
        df_filtrado = df.copy()

        if isinstance(intervalo_datas, tuple) and len(intervalo_datas) == 2:
            data_inicio, data_fim = intervalo_datas
            df_filtrado = df_filtrado[
                (df_filtrado["Date"].dt.date >= data_inicio) &
                (df_filtrado["Date"].dt.date <= data_fim)
            ]

        if categorias_selecionadas:
            df_filtrado = df_filtrado[df_filtrado["SKU_Category"].isin(categorias_selecionadas)]
        else:
            df_filtrado = df_filtrado.iloc[0:0]

        if skus_selecionados:
            df_filtrado = df_filtrado[df_filtrado["SKU"].isin(skus_selecionados)]
        else:
            df_filtrado = df_filtrado.iloc[0:0]

        if df_filtrado.empty:
            st.warning("Nenhum dado encontrado para os filtros selecionados.")
            st.stop()

        # =========================
        # KPIs
        # =========================
        total_faturamento = df_filtrado["Sales_Amount"].sum()
        total_quantidade = df_filtrado["Quantity"].sum()
        total_transacoes = df_filtrado["Transaction_ID"].nunique()
        total_clientes = df_filtrado["Customer_ID"].nunique()
        total_categorias = df_filtrado["SKU_Category"].nunique()
        total_skus = df_filtrado["SKU"].nunique()
        ticket_medio = total_faturamento / total_transacoes if total_transacoes > 0 else 0

        st.subheader("Indicadores Principais")

        col1, col2, col3 = st.columns(3)
        col1.metric("Faturamento Total", f"R$ {total_faturamento:,.2f}")
        col2.metric("Quantidade Vendida", f"{total_quantidade:,.0f}")
        col3.metric("Ticket Médio", f"R$ {ticket_medio:,.2f}")

        col4, col5, col6 = st.columns(3)
        col4.metric("Transações", total_transacoes)
        col5.metric("Clientes Únicos", total_clientes)
        col6.metric("Categorias", total_categorias)

        st.metric("SKUs Únicos", total_skus)

        # =========================
        # DADOS FILTRADOS
        # =========================
        st.subheader("Prévia dos Dados Filtrados")
        st.dataframe(df_filtrado, use_container_width=True)

        # =========================
        # GRÁFICOS
        # =========================
        faturamento_tempo = (
            df_filtrado.groupby("Date", as_index=False)["Sales_Amount"]
            .sum()
            .sort_values("Date")
        )

        st.subheader("Evolução do Faturamento ao Longo do Tempo")
        st.line_chart(faturamento_tempo.set_index("Date"))

        quantidade_tempo = (
            df_filtrado.groupby("Date", as_index=False)["Quantity"]
            .sum()
            .sort_values("Date")
        )

        st.subheader("Evolução da Quantidade Vendida ao Longo do Tempo")
        st.line_chart(quantidade_tempo.set_index("Date"))

        faturamento_categoria = (
            df_filtrado.groupby("SKU_Category", as_index=False)["Sales_Amount"]
            .sum()
            .sort_values("Sales_Amount", ascending=False)
        )

        st.subheader("Faturamento por Categoria")
        st.bar_chart(faturamento_categoria.set_index("SKU_Category"))

        quantidade_categoria = (
            df_filtrado.groupby("SKU_Category", as_index=False)["Quantity"]
            .sum()
            .sort_values("Quantity", ascending=False)
        )

        st.subheader("Quantidade Vendida por Categoria")
        st.bar_chart(quantidade_categoria.set_index("SKU_Category"))

        top_skus_faturamento = (
            df_filtrado.groupby("SKU", as_index=False)["Sales_Amount"]
            .sum()
            .sort_values("Sales_Amount", ascending=False)
            .head(10)
        )

        st.subheader("Top 10 SKUs por Faturamento")
        st.bar_chart(top_skus_faturamento.set_index("SKU"))

        top_skus_quantidade = (
            df_filtrado.groupby("SKU", as_index=False)["Quantity"]
            .sum()
            .sort_values("Quantity", ascending=False)
            .head(10)
        )

        st.subheader("Top 10 SKUs por Quantidade Vendida")
        st.bar_chart(top_skus_quantidade.set_index("SKU"))

        resumo_categoria = (
            df_filtrado.groupby("SKU_Category", as_index=False)
            .agg({
                "Sales_Amount": "sum",
                "Quantity": "sum",
                "Transaction_ID": "nunique",
                "Customer_ID": "nunique"
            })
            .rename(columns={
                "Transaction_ID": "Transacoes",
                "Customer_ID": "Clientes_Unicos"
            })
            .sort_values("Sales_Amount", ascending=False)
        )

        st.subheader("Resumo por Categoria")
        st.dataframe(resumo_categoria, use_container_width=True)

    except Exception as e:
        st.error(f"Ocorreu um erro ao processar os dados: {e}")

else:
    st.info("Aguardando carregamento da planilha.") 