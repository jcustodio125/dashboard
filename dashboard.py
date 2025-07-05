import streamlit as st
import pandas as pd
import plotly.express as px
import requests

# Configuração da página
st.set_page_config(page_title="Dashboard de Vendas", layout="wide")

st.markdown("""
    <style>
    .block-container {
        padding-top: 2rem;
        padding-bottom: 2rem;
        padding-left: 2rem;
        padding-right: 2rem;
    }
    </style>
""", unsafe_allow_html=True)

st.title("📊 Dashboard de Vendas")

# === Carregar dados da API ===
url = "http://127.0.0.1:8000/vendas"

with st.spinner("🔄 Carregando dados da API..."):
    try:
        resposta = requests.get(url)
        resposta.raise_for_status()
        data = resposta.json()
    except Exception as e:
        st.error(f"❌ Falha ao acessar a API: {e}")
        st.stop()

df = pd.DataFrame(data)
df["data"] = pd.to_datetime(df["data"])

# Copiar o DataFrame original para manter os filtros consistentes
df_original = df.copy()

# === Sidebar com filtros ===
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/891/891462.png", width=80)
    st.title("🔧 Filtros")

    data_ini = st.date_input("Data inicial", value=df["data"].min().date())
    data_fim = st.date_input("Data final", value=df["data"].max().date())

    produtos_unicos = sorted(df_original["produto"].unique())
    regioes_unicas = sorted(df_original["regiao"].unique())

    produtos = st.multiselect(
        "🛍 Produtos",
        options=produtos_unicos,
        default=produtos_unicos
    )

    regioes = st.multiselect(
        "🌍 Regiões",
        options=regioes_unicas,
        default=regioes_unicas
    )

    num_produtos = st.slider("🔢 Nº de produtos no gráfico de barras", 3, 20, 10)
    tamanho = st.slider("📐 Tamanho do layout (colunas)", 3, 9, 6)
    st.divider()
    mostrar_linha = st.checkbox("📈 Gráfico de Linha (por dia)", value=True)
    mostrar_barras = st.checkbox("📊 Gráfico de Barras (top produtos)", value=True)
    mostrar_pizza = st.checkbox("🥧 Gráfico de Pizza (por região)", value=True)

# === Aplicar os filtros ===
df_filtrado = df[
    (df["data"] >= pd.to_datetime(data_ini)) &
    (df["data"] <= pd.to_datetime(data_fim)) &
    (df["produto"].isin(produtos)) &
    (df["regiao"].isin(regioes))
]

# === Indicadores ===
st.subheader("📌 Indicadores Gerais")
col1, col2, col3 = st.columns(3)

total_vendas = df_filtrado["valor"].sum()
total_qtd = df_filtrado["quantidade"].sum()
ticket_medio = total_vendas / total_qtd if total_qtd > 0 else 0

col1.metric("💰 Total Vendido", f"R$ {total_vendas:,.2f}")
col2.metric("📦 Vendas Realizadas", total_qtd)
col3.metric("🧾 Ticket Médio", f"R$ {ticket_medio:,.2f}")

st.divider()

# === Layout de gráficos ===
colA, colB = st.columns([tamanho, max(1, 12 - tamanho)])

if mostrar_linha:
    with colA:
        st.subheader("📈 Vendas por Dia")
        vendas_dia = df_filtrado.groupby("data")["valor"].sum().reset_index()
        fig_linha = px.line(
            vendas_dia,
            x="data",
            y="valor",
            title="Total de Vendas por Dia",
            markers=True,
            labels={"data": "Data", "valor": "Valor (R$)"}
        )
        fig_linha.update_layout(hovermode="x unified")
        st.plotly_chart(fig_linha, use_container_width=True)

if mostrar_barras:
    with colB:
        st.subheader(f"📊 Top {num_produtos} Produtos Vendidos")
        vendas_produto = df_filtrado.groupby("produto")["valor"].sum().reset_index()
        vendas_produto = vendas_produto.sort_values("valor", ascending=False).head(num_produtos)

        fig_barra = px.bar(
            vendas_produto,
            x="produto",
            y="valor",
            text_auto=".2s",
            labels={"valor": "Valor (R$)", "produto": "Produto"}
        )
        st.plotly_chart(fig_barra, use_container_width=True)

        with st.expander("📋 Ver Tabela de Produtos"):
            st.dataframe(vendas_produto, use_container_width=True)

if mostrar_pizza:
    st.subheader("🥧 Distribuição de Vendas por Região")
    vendas_regiao = df_filtrado.groupby("regiao")["valor"].sum().reset_index()
    fig_pizza = px.pie(vendas_regiao, values="valor", names="regiao", title="Participação por Região")
    st.plotly_chart(fig_pizza, use_container_width=True)

# === Download dos dados ===
with st.expander("⬇️ Baixar Dados Filtrados"):
    csv = df_filtrado.to_csv(index=False).encode("utf-8")
    st.download_button("📥 Baixar CSV", csv, "vendas_filtradas.csv", "text/csv")
