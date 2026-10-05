import streamlit as st
import pandas as pd
import plotly.express as px

# =====================================================
# CONFIGURAÇÃO
# =====================================================

st.set_page_config(
    page_title="Sabor do Sertão",
    layout="wide"
)

st.title("Sabor do Sertão")
st.subheader("Painel de Análise de Vendas")


# =====================================================
# CARREGAMENTO DOS DADOS
# =====================================================

df = pd.read_csv("vendas_sabor_do_sertao.csv")

df["data"] = pd.to_datetime(df["data"])

# Tratamento dos valores ausentes
df["avaliacao"] = df["avaliacao"].fillna(
    df["avaliacao"].median()
)


# =====================================================
# FILTROS
# =====================================================

st.sidebar.header("Filtros")

cidades = st.sidebar.multiselect(
    "Cidade",
    options=sorted(df["cidade"].unique()),
    default=sorted(df["cidade"].unique())
)

categorias = st.sidebar.multiselect(
    "Categoria",
    options=sorted(df["categoria"].unique()),
    default=sorted(df["categoria"].unique())
)

data_inicial = df["data"].min().date()
data_final = df["data"].max().date()

periodo = st.sidebar.date_input(
    "Período",
    value=(data_inicial, data_final),
    min_value=data_inicial,
    max_value=data_final
)

df_filtrado = df[
    (df["cidade"].isin(cidades)) &
    (df["categoria"].isin(categorias))
].copy()

if len(periodo) == 2:
    inicio = pd.to_datetime(periodo[0])
    fim = pd.to_datetime(periodo[1])

    df_filtrado = df_filtrado[
        (df_filtrado["data"] >= inicio) &
        (df_filtrado["data"] <= fim)
    ]


# =====================================================
# INDICADORES
# =====================================================

st.header("Indicadores")

faturamento = df_filtrado["total"].sum()
numero_vendas = len(df_filtrado)

if numero_vendas > 0:
    ticket_medio = faturamento / numero_vendas
    avaliacao_media = df_filtrado["avaliacao"].mean()
else:
    ticket_medio = 0
    avaliacao_media = 0

col1, col2, col3, col4 = st.columns(4)

col1.metric(
    "Faturamento total",
    f"R$ {faturamento:,.2f}"
)

col2.metric(
    "Número de vendas",
    numero_vendas
)

col3.metric(
    "Ticket médio",
    f"R$ {ticket_medio:,.2f}"
)

col4.metric(
    "Avaliação média",
    f"{avaliacao_media:.2f}"
)


# =====================================================
# GRÁFICOS
# =====================================================

st.header("Análise das vendas")

tab1, tab2, tab3, tab4 = st.tabs([
    "Faturamento mensal",
    "Cidades",
    "Produtos",
    "Pagamentos"
])


# GRÁFICO 1
with tab1:

    mensal = (
        df_filtrado
        .groupby(
            df_filtrado["data"].dt.to_period("M")
        )["total"]
        .sum()
        .reset_index()
    )

    mensal["data"] = mensal["data"].astype(str)

    fig = px.line(
        mensal,
        x="data",
        y="total",
        markers=True,
        title="Faturamento mensal"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )


# GRÁFICO 2
with tab2:

    por_cidade = (
        df_filtrado
        .groupby("cidade")["total"]
        .sum()
        .reset_index()
        .sort_values(
            "total",
            ascending=False
        )
    )

    fig = px.bar(
        por_cidade,
        x="cidade",
        y="total",
        title="Faturamento por cidade"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )


# GRÁFICO 3
with tab3:

    produtos = (
        df_filtrado
        .groupby("produto")["quantidade"]
        .sum()
        .nlargest(5)
        .reset_index()
    )

    fig = px.bar(
        produtos,
        x="quantidade",
        y="produto",
        orientation="h",
        title="Top 5 produtos mais vendidos"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )


# GRÁFICO 4
with tab4:

    pagamentos = (
        df_filtrado["pagamento"]
        .value_counts()
        .reset_index()
    )

    pagamentos.columns = [
        "pagamento",
        "quantidade"
    ]

    fig = px.pie(
        pagamentos,
        names="pagamento",
        values="quantidade",
        title="Formas de pagamento"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )


# =====================================================
# EXPLORAÇÃO DOS DADOS
# =====================================================

st.header("Exploração dos dados")

st.subheader("Primeiras linhas")

st.dataframe(
    df_filtrado.head()
)

st.subheader("Resumo estatístico")

st.dataframe(
    df_filtrado.describe()
)

st.subheader("Valores ausentes")

st.dataframe(
    df_filtrado.isnull().sum()
)

st.caption(
    "Os valores ausentes da coluna avaliação foram "
    "preenchidos com a mediana para preservar os registros "
    "sem sofrer grande influência de valores extremos."
)


# =====================================================
# INSIGHTS
# =====================================================

st.header("Insights")

if not df_filtrado.empty:

    melhor_cidade = (
        df_filtrado
        .groupby("cidade")["total"]
        .sum()
        .idxmax()
    )

    produto_mais_vendido = (
        df_filtrado
        .groupby("produto")["quantidade"]
        .sum()
        .idxmax()
    )

    pagamento_principal = (
        df_filtrado["pagamento"]
        .value_counts()
        .idxmax()
    )

    st.markdown(
        f"""
        - **{melhor_cidade}** apresenta o maior faturamento no período selecionado.
        - **{produto_mais_vendido}** é o produto mais vendido em quantidade.
        - **{pagamento_principal}** é a forma de pagamento mais utilizada.
        """
    )

else:
    st.warning(
        "Não existem dados para os filtros selecionados."
    )


# =====================================================
# DOWNLOAD
# =====================================================

csv = df_filtrado.to_csv(
    index=False
).encode("utf-8")

st.download_button(
    label="Baixar dados filtrados",
    data=csv,
    file_name="vendas_filtradas.csv",
    mime="text/csv"
)

# =====================================================
# EXPLORADOR LIVRE - BÔNUS
# =====================================================

st.header("Explorador livre")

st.write(
    "Escolha as colunas e o tipo de gráfico para explorar os dados."
)

eixo_x = st.selectbox(
    "Eixo X",
    df_filtrado.columns
)

eixo_y = st.selectbox(
    "Eixo Y",
    df_filtrado.columns
)

tipo_grafico = st.selectbox(
    "Tipo de gráfico",
    ["Barras", "Linha", "Dispersão"]
)

if tipo_grafico == "Barras":

    fig_livre = px.bar(
        df_filtrado,
        x=eixo_x,
        y=eixo_y
    )

elif tipo_grafico == "Linha":

    fig_livre = px.line(
        df_filtrado,
        x=eixo_x,
        y=eixo_y
    )

else:

    fig_livre = px.scatter(
        df_filtrado,
        x=eixo_x,
        y=eixo_y
    )

st.plotly_chart(
    fig_livre,
    use_container_width=True
)