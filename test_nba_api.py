from nba_api.stats.static import players
from nba_api.stats.endpoints import playergamelog

all_players = players.get_players()

lebron = [p for p in all_players if p["full_name"] == "LeBron James"][0]
player_id = lebron["id"]

print("Player ID:", player_id)

gamelog = playergamelog.PlayerGameLog(
    player_id=player_id,
    season="2024-25"
)

df = gamelog.get_data_frames()[0]
print(df.head())