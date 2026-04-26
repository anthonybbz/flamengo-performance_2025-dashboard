import pandas as pd
import requests
import numpy as np
import os

# ======================
# CONFIGURAÇÕES
# ======================
API_KEY = os.getenv("FOOTBALL_DATA_API_KEY")
URL = "https://api.football-data.org/v4/competitions/BSA/matches?season=2025"

headers = {
    "X-Auth-Token": API_KEY
}

# ======================
# COLETA DE DADOS
# ======================
response = requests.get(URL, headers=headers)
data = response.json()
matches = data["matches"]

df = pd.json_normalize(matches)

# ======================
# FILTRO FLAMENGO
# ======================
flamengo_df = df[
    (df["homeTeam.name"] == "CR Flamengo") |
    (df["awayTeam.name"] == "CR Flamengo")
]

flamengo_df = flamengo_df[
    [
        "utcDate",
        "competition.name",
        "homeTeam.shortName",
        "awayTeam.shortName",
        "score.fullTime.home",
        "score.fullTime.away",
        "score.halfTime.home",
        "score.halfTime.away",
    ]
]

# ======================
# ENGENHARIA DE DADOS
# ======================
flamengo_df["Gols Feitos Resultado Intervalo"] = np.where(
    flamengo_df["homeTeam.shortName"] == "Flamengo",
    flamengo_df["score.halfTime.home"],
    flamengo_df["score.halfTime.away"],
)

flamengo_df["Gols Sofridos Resultado Intervalo"] = np.where(
    flamengo_df["homeTeam.shortName"] == "Flamengo",
    flamengo_df["score.halfTime.away"],
    flamengo_df["score.halfTime.home"],
)

flamengo_df["Resultado Intervalo"] = np.where(
    flamengo_df["Gols Feitos Resultado Intervalo"]
    > flamengo_df["Gols Sofridos Resultado Intervalo"],
    "Vitória",
    np.where(
        flamengo_df["Gols Feitos Resultado Intervalo"]
        < flamengo_df["Gols Sofridos Resultado Intervalo"],
        "Derrota",
        "Empate",
    ),
)

flamengo_df["Gols Feitos Resultado Final"] = np.where(
    flamengo_df["homeTeam.shortName"] == "Flamengo",
    flamengo_df["score.fullTime.home"],
    flamengo_df["score.fullTime.away"],
)

flamengo_df["Gols Sofridos Resultado Final"] = np.where(
    flamengo_df["homeTeam.shortName"] == "Flamengo",
    flamengo_df["score.fullTime.away"],
    flamengo_df["score.fullTime.home"],
)

flamengo_df["Resultado Final"] = np.where(
    flamengo_df["Gols Feitos Resultado Final"]
    > flamengo_df["Gols Sofridos Resultado Final"],
    "Vitória",
    np.where(
        flamengo_df["Gols Feitos Resultado Final"]
        < flamengo_df["Gols Sofridos Resultado Final"],
        "Derrota",
        "Empate",
    ),
)

flamengo_df["Pontos"] = np.where(
    flamengo_df["Resultado Final"] == "Vitória",
    3,
    np.where(flamengo_df["Resultado Final"] == "Derrota", 0, 1),
)

# ======================
# EXPORTAÇÃO
# ======================
flamengo_df["utcDate"] = (
    pd.to_datetime(flamengo_df["utcDate"])
    .dt.tz_localize("UTC")
    .dt.tz_convert("America/Sao_Paulo")
)

flamengo_df = flamengo_df.rename(columns={
    "utcDate": "Data/Hora",
    "competition.name": "Competicao",
    "homeTeam.shortName": "Time da Casa",
    "awayTeam.shortName": "Time de Fora",
})

flamengo_df["Adversario"] = np.where(
    flamengo_df["Time da Casa"] == "Flamengo",
    flamengo_df["Time de Fora"],
    flamengo_df["Time da Casa"],
)

flamengo_df.to_csv(
    "flamengo_jogos_2025.csv",
    index=False,
    encoding="ISO-8859-1"
)
