import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

#configuração
st.set_page_config(
    page_title="Análise de Desempenho - Flamengo",
    layout="wide"
)
# css
st.markdown("""
<style>
.stApp {
    background-color: #0e0e0e;
    color: white;
}

/* MÉTRICA (cards) */
section[data-testid="stMetric"] {
    background-color: #1c1c1c;
    padding: 16px;
    border-radius: 10px;
    border-top: 4px solid #cc0000;
    text-align: center;
}

/* LABEL da métrica */
section[data-testid="stMetric"] label {
    color: #ffffff !important;
    font-size: 14px;
}

/* VALOR da métrica */
section[data-testid="stMetric"] div {
    color: #ffffff !important;
    font-size: 32px;
    font-weight: bold;
}
</style>
""", unsafe_allow_html=True)


# carregar dados
df = pd.read_csv(
    "01_coleta_e_excel/flamengo_jogos_2025.csv",
    encoding="latin-1


# KPIs
jogos = len(df)
vitorias = (df["Resultado Final"] == "Vitória").sum()
empates = (df["Resultado Final"] == "Empate").sum()
derrotas = (df["Resultado Final"] == "Derrota").sum()
pontos = vitorias * 3 + empates
aproveitamento = vitorias / jogos

# título
st.title("Análise de Desempenho - Flamengo")

# layout
col1, col2, col3, col4, col5, col6 = st.columns(6)

col1.metric("Jogos", jogos)
col2.metric("Vitórias", vitorias)
col3.metric("Empates", empates)
col4.metric("Derrotas", derrotas)
col5.metric("Pontos", pontos)
col6.metric("Aproveitamento", f"{aproveitamento:.0%}")

st.markdown("---")
# gráficos
col_g1,col_g2 = st.columns(2)

#gols feitos x sofridos
gols_feitos = df["Gols Feitos Resultado Final"].sum()
gols_sofridos = df["Gols Sofridos Resultado Final"].sum()
with col_g1:
    st.subheader("Gols Feitos x Gols Sofridos")
    fig, ax = plt.subplots()
    
    categorias = ["Feitos", "Sofridos"]
    valores = [gols_feitos, gols_sofridos]
    cores = ["#00c853", "#d50000"]

    barras = ax.bar(categorias, valores, color=cores)

    # fundo escuro
    ax.set_facecolor("#0e0e0e")
    fig.patch.set_facecolor("#0e0e0e")

    # cor dos eixos
    ax.tick_params(colors="white")
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.spines["left"].set_color("white")
    ax.spines["bottom"].set_color("white")

    
    for barra in barras:
        altura = barra.get_height()
        ax.text(
            barra.get_x() + barra.get_width() / 2,
            altura + 1,                      
            f"{int(altura)}",
            ha="center",
            va="bottom",
            color="white",
            fontsize=14,
            fontweight="bold"
        )

    st.pyplot(fig)


with col_g2:
    st.subheader("Resultado Intervalo x Resultado Final")

    # contar valores da coluna Analise
    analise_df = (
        df["Analise"]
        .value_counts()
        .reset_index()
    )
    analise_df.columns = ["Analise", "Qtd"]

    fig, ax = plt.subplots(figsize=(8, 4))

    barras = ax.barh(
        analise_df["Analise"],
        analise_df["Qtd"],
        color="#cc0000"
    )

    # fundo escuro
    ax.set_facecolor("#0e0e0e")
    fig.patch.set_facecolor("#0e0e0e")

    # estilo dos eixos
    ax.tick_params(axis="x", colors="white")
    ax.tick_params(axis="y", colors="white")
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.spines["left"].set_color("white")
    ax.spines["bottom"].set_color("white")

    # maior em cima (igual Power BI)
    ax.invert_yaxis()

    # valores nas barras
    for barra in barras:
        largura = barra.get_width()
        ax.text(
            largura + 0.2,
            barra.get_y() + barra.get_height() / 2,
            f"{int(largura)}",
            va="center",
            ha="left",
            color="white",
            fontsize=12,
            fontweight="bold"
        )

    st.pyplot(fig)


# tabela
st.subheader("Jogos")
st.dataframe(
    df,
    use_container_width=True,
    hide_index=True)
