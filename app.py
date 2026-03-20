import streamlit as st
import pandas as pd

st.set_page_config(page_title="Dashboard de Preços", layout="wide")

st.title("Dashboard de Sensibilidade a Preço")
st.write("Análise inicial de vendas, preço e comportamento transacional.")

uploaded_file = st.file_uploader("Envie sua planilha Excel", type=["xlsx"])

if uploaded_file is not None:
    df = pd.read_excel(uploaded_file)

    # Tratamento básico
    df["Date"] = pd.to_datetime(df["Date"], errors="coerce")

    # KPIs principais
    total_faturamento = df["Sales_Amount"].sum()
    total_quantidade = df["Quantity"].sum()
    total_transacoes = df["Transaction_ID"].nunique()
    total_clientes = df["Customer_ID"].nunique()
    preco_medio = df["price"].mean()
    ticket_medio = total_faturamento / total_transacoes if total_transacoes > 0 else 0

    col1, col2, col3 = st.columns(3)
    col1.metric("Faturamento Total", f"R$ {total_faturamento:,.2f}")
    col2.metric("Quantidade Vendida", f"{total_quantidade:,}")
    col3.metric("Preço Médio", f"R$ {preco_medio:,.2f}")

    col4, col5, col6 = st.columns(3)
    col4.metric("Transações", total_transacoes)
    col5.metric("Clientes Únicos", total_clientes)
    col6.metric("Ticket Médio", f"R$ {ticket_medio:,.2f}")

    st.subheader("Prévia dos dados")
    st.dataframe(df, use_container_width=True)

    # Faturamento por data
    faturamento_tempo = (
        df.groupby("Date", as_index=False)["Sales_Amount"]
        .sum()
        .sort_values("Date")
    )

    st.subheader("Evolução do Faturamento ao Longo do Tempo")
    st.line_chart(faturamento_tempo.set_index("Date"))

    # Quantidade por data
    quantidade_tempo = (
        df.groupby("Date", as_index=False)["Quantity"]
        .sum()
        .sort_values("Date")
    )

    st.subheader("Evolução da Quantidade Vendida ao Longo do Tempo")
    st.line_chart(quantidade_tempo.set_index("Date"))

    # Preço médio por data
    preco_tempo = (
        df.groupby("Date", as_index=False)["price"]
        .mean()
        .sort_values("Date")
    )

    st.subheader("Evolução do Preço Médio ao Longo do Tempo")
    st.line_chart(preco_tempo.set_index("Date"))

    # Relação entre preço e quantidade
    relacao_preco_quantidade = (
        df.groupby("price", as_index=False)["Quantity"]
        .sum()
        .sort_values("price")
    )

    st.subheader("Relação entre Preço e Quantidade Vendida")
    st.line_chart(relacao_preco_quantidade.set_index("price"))

    # Relação entre preço e faturamento
    relacao_preco_faturamento = (
        df.groupby("price", as_index=False)["Sales_Amount"]
        .sum()
        .sort_values("price")
    )

    st.subheader("Relação entre Preço e Faturamento")
    st.line_chart(relacao_preco_faturamento.set_index("price"))

else:
    st.info("Aguardando upload da planilha.")