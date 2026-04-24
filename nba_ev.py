import pandas as pd
import numpy as np


# 🔎 mock de dados (substituível por nba_api depois)
def fetch_player_gamelog(player: str):
    data = {
        "PTS": [25, 30, 22, 28, 35, 18, 40, 27, 29, 31],
        "REB": [8, 10, 7, 9, 11, 6, 12, 8, 9, 10],
        "AST": [6, 5, 7, 8, 6, 4, 9, 7, 6, 8],
    }

    return pd.DataFrame(data)


# 🎯 peso maior para jogos recentes (form)
def weighted_mean(values):
    weights = np.arange(1, len(values) + 1)
    return np.average(values, weights=weights)


# 🛡️ desvio padrão robusto
def safe_std(values):
    std = np.std(values)

    # evita modelo quebrar
    if std == 0 or np.isnan(std):
        return max(np.mean(values) * 0.1, 1)  # fallback inteligente

    return std


# ⚔️ ajuste simples por adversário
def opponent_adjustment(opp: str):
    weak_defense = ["CHA", "WAS", "DET"]
    strong_defense = ["BOS", "MIN", "NYK"]

    if opp in weak_defense:
        return 1.05
    elif opp in strong_defense:
        return 0.95
    return 1.0


# 🎲 simulação Monte Carlo robusta
def monte_carlo_prob(mean, std, line, side, simulations=10000):
    sims = np.random.normal(mean, std, simulations)

    if side == "over":
        prob = np.mean(sims > line)
    else:
        prob = np.mean(sims < line)

    # proteção total
    if np.isnan(prob):
        return 0.5

    return float(prob)


# 📊 função principal
def analyze(bet: dict, df: pd.DataFrame):
    try:
        market = bet.get("market")
        line = float(bet.get("line", 0))
        odd = float(bet.get("odd", 0))
        side = bet.get("side", "over").lower()
        opp = bet.get("opp", "")

        if df is None or df.empty:
            return {"error": "Sem dados"}

        # 📦 cria PRA se necessário
        if market == "PRA":
            if all(col in df.columns for col in ["PTS", "REB", "AST"]):
                df["PRA"] = df["PTS"] + df["REB"] + df["AST"]
            else:
                return {"error": "Dados insuficientes para PRA"}

        if market not in df.columns:
            return {"error": f"Market inválido: {market}"}

        values = df[market].dropna().values

        if len(values) < 3:
            return {"error": "Amostra pequena demais"}

        # 📈 média ponderada (form recente)
        mean = weighted_mean(values)

        # ⚔️ ajuste por adversário
        adj_factor = opponent_adjustment(opp)
        adjusted_mean = mean * adj_factor

        # 📉 desvio padrão robusto
        std = safe_std(values)

        # 🎲 Monte Carlo
        prob = monte_carlo_prob(adjusted_mean, std, line, side)

        # 🎯 prob implícita
        implied_prob = 1 / odd if odd > 0 else 0

        # 💰 EV correto
        ev = (prob * odd) - 1

        # 🧠 edge
        edge = prob - implied_prob

        # 🧾 decisão
        decision = "VALUE BET" if ev > 0 else "NO BET"

        return {
            "player": bet.get("player"),
            "market": market,
            "line": line,
            "odd": odd,
            "side": side,

            "adjusted_mean": round(float(adjusted_mean), 2),
            "std_dev": round(float(std), 2),

            "model_probability": round(prob * 100, 2),
            "implied_probability": round(implied_prob * 100, 2),
            "edge": round(edge * 100, 2),
            "ev": round(ev * 100, 2),

            "sample_size": len(values),
            "simulations": 10000,

            "decision": decision
        }

    except Exception as e:
        return {"error": str(e)}