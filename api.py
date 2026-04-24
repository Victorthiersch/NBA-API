from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware

# importa seu script
from nba_ev import fetch_player_gamelog, analyze

app = FastAPI()

# 🚨 LIBERA CORS (ESSENCIAL PARA O LOVABLE)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # pode restringir depois
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 📦 estrutura do request
class Bet(BaseModel):
    player: str
    market: str   # PTS, REB, AST, PRA
    line: float
    odd: float
    side: str = "over"
    team: str = "LAL"
    opp: str = "BOS"
    home: bool = True


# 🔍 rota de teste (IMPORTANTE)
@app.get("/")
def root():
    return {"status": "API ONLINE"}


# 🌐 endpoint principal
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