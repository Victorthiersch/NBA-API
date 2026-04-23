from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from nba_ev import fetch_player_gamelog, analyze

app = FastAPI()

# 🌐 CORS (obrigatório para Lovable funcionar)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # pode restringir depois para segurança
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 📦 modelo da aposta
class Bet(BaseModel):
    player: str
    market: str   # PTS, REB, AST, PRA
    line: float
    odd: float
    side: str = "over"
    team: str = "LAL"
    opp: str = "BOS"
    home: bool = True


# 🟢 endpoint principal (Lovable usa esse)
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


# 🟢 health check (evita "Not Found")
@app.get("/")
def home():
    return {
        "status": "ok",
        "message": "NBA API is running"
    }