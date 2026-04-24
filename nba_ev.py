import pandas as pd
import numpy as np


# =========================
# 📦 MOCK (substituir depois por nba_api)
# =========================
def fetch_player_gamelog(player: str):
    np.random.seed(hash(player) % 10000)

    data = {
        "PTS": np.random.normal(25, 6, 30),
        "REB": np.random.normal(6, 2, 30),
        "AST": np.random.normal(5, 2, 30),
    }

    return pd.DataFrame(data)


# =========================
# 🧠 PESO EXPONENCIAL (FORMA RECENTE)
# =========================
def exponential_weights(n, decay=0.85):
    return np.array([decay ** (n - i) for i in range(n)])


def weighted_mean(values):
    w = exponential_weights(len(values))
    return np.average(values, weights=w)


def weighted_std(values):
    w = exponential_weights(len(values))
    mean = np.average(values, weights=w)
    variance = np.average((values - mean) ** 2, weights=w)
    return np.sqrt(variance)


# =========================
# 🏀 AJUSTE POR CONTEXTO
# =========================
def adjust_for_context(mean, home, opp_strength=1.0):
    """
    opp_strength:
        <1 = defesa fraca (melhora stats)
        >1 = defesa forte (piora stats)
    """

    home_boost = 1.03 if home else 0.97

    return mean * home_boost * opp_strength


# =========================
# 🎲 MONTE CARLO PROFISSIONAL
# =========================
def monte_carlo(mean, std, line, side, simulations=20000):
    sims = np.random.normal(mean, std, simulations)

    if side == "over":
        return np.mean(sims > line)
    else:
        return np.mean(sims < line)


# =========================
# 📊 MAIN MODEL
# =========================
def analyze(bet: dict, df: pd.DataFrame):
    try:
        market = bet["market"]
        line = float(bet["line"])
        odd = float(bet["odd"])
        side = bet.get("side", "over")
        home = bet.get("home", True)
        opp = bet.get("opp", "AVG")

        if df is None or df.empty:
            return {"error": "Sem dados"}

        # PRA
        if market == "PRA":
            df["PRA"] = df["PTS"] + df["REB"] + df["AST"]

        if market not in df.columns:
            return {"error": f"Market inválido: {market}"}

        values = df[market].dropna().values

        if len(values) < 5:
            return {"error": "Amostra insuficiente"}

        # =========================
        # 📈 ESTATÍSTICAS BASE
        # =========================
        mean = weighted_mean(values)
        std = weighted_std(values)

        std = max(std, 1.0)  # proteção

        # =========================
        # 🧠 AJUSTE POR ADVERSÁRIO (SIMPLIFICADO)
        # =========================
        opp_map = {
            "PHI": 1.02,
            "BOS": 0.98,
            "LAL": 1.00,
            "DEF_STRONG": 1.05,
            "DEF_WEAK": 0.95
        }

        opp_strength = opp_map.get(opp, 1.0)

        adjusted_mean = adjust_for_context(mean, home, opp_strength)

        # =========================
        # 🎲 PROBABILIDADE (MONTE CARLO)
        # =========================
        prob = monte_carlo(adjusted_mean, std, line, side)

        # =========================
        # 💰 MÉTRICAS FINANCEIRAS
        # =========================
        implied = 1 / odd if odd > 0 else 0
        ev = (prob * odd) - 1
        edge = prob - implied

        # proteção numérica
        prob = float(np.clip(prob, 0, 1))
        ev = float(np.nan_to_num(ev))
        edge = float(np.nan_to_num(edge))

        decision = "VALUE BET" if ev > 0 else "NO BET"

        return {
            "player": bet["player"],
            "market": market,
            "line": line,
            "odd": odd,
            "side": side,

            # 📊 CORE
            "adjusted_mean": round(float(adjusted_mean), 2),
            "std_dev": round(float(std), 2),

            # 🎯 PROBABILIDADES
            "model_probability": round(prob * 100, 2),
            "implied_probability": round(implied * 100, 2),
            "edge": round(edge * 100, 2),

            # 💰 EV
            "ev": round(ev * 100, 2),

            # ⚙️ META
            "sample_size": len(values),
            "simulations": 20000,
            "home": home,
            "opp": opp,

            # 🧠 RESULTADO
            "decision": decision
        }

    except Exception as e:
        return {"error": str(e)}