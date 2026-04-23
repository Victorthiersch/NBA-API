import pandas as pd


# 🔎 Busca histórico do jogador (placeholder simples)
def fetch_player_gamelog(player: str):
    """
    Aqui você pode futuramente integrar:
    - nba_api
    - base CSV
    - banco de dados

    Por enquanto, vamos simular dados.
    """

    data = {
        "PTS": [25, 30, 22, 28, 35],
        "REB": [8, 10, 7, 9, 11],
        "AST": [6, 5, 7, 8, 6],
    }

    df = pd.DataFrame(data)
    return df


# 📊 Função principal de análise EV
def analyze(bet: dict, df: pd.DataFrame):
    """
    Calcula probabilidade simples baseada no histórico
    e compara com a linha da bet.
    """

    market = bet["market"]
    line = bet["line"]
    odd = bet["odd"]
    side = bet["side"]

    if market not in df.columns:
        return {
            "error": f"Market {market} não encontrado no histórico"
        }

    # 📈 média do jogador
    avg = df[market].mean()

    # 📊 probabilidade simples (heurística)
    if side == "over":
        prob = (df[market] > line).mean()
    else:
        prob = (df[market] < line).mean()

    # 💰 EV (expected value)
    ev = (prob * (odd - 1)) - (1 - prob)

    # 🧠 decisão
    if ev > 0:
        decision = "BET VALUE"
    else:
        decision = "NO BET"

    return {
        "player": bet["player"],
        "market": market,
        "line": line,
        "odd": odd,
        "side": side,
        "average": float(avg),
        "probability": float(prob),
        "ev": float(ev),
        "decision": decision
    }