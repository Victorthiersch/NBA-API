from fastapi import FastAPI
from pydantic import BaseModel

# importa seu script
from nba_ev import fetch_player_gamelog, analyze

app = FastAPI()


# 📦 estrutura do que você vai receber do Lovable
class Bet(BaseModel):
    player: str
    market: str   # PTS, REB, AST, PRA
    line: float
    odd: float
    side: str = "over"
    team: str = "LAL"
    opp: str = "BOS"
    home: bool = True


# 🌐 endpoint (API)
@app.post("/analyze")
def analyze_bet(bet: Bet):
    df = fetch_player_gamelog(bet.player)

    result = analyze(
        {
            "player": bet.player,
            "market": bet.market,
            "line": bet.line,
            "odd": bet.odd,
            "side": bet.side,
            "team": bet.team,
            "opp": bet.opp,
            "home": bet.home
        },
        df
    )

    return result
    
    if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)