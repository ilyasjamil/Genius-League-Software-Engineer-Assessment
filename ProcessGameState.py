import pandas as pd
import pyarrow

class ProcessGameState:


    def __init__(self, file_path) -> None:
        self.file_path = file_path
        self.df = pd.DataFrame()

    def ingest_file(self):
        self.df = pd.read_parquet(self.file_path)

    def get_team_side_data(self, team, side):
        return self.df[(self.df['team'] == team) & (self.df['side'] == side)]


    def check_player_boundaries(self, df, boundaries):
        minX = boundaries[0]
        maxX = boundaries[1]
        minY = boundaries[2]
        maxY = boundaries[3]
        minZ = boundaries[4]
        maxZ = boundaries[5]
        is_within_boundaries = []

        for i, row in df.iterrows():
            
            x = row['x']
            y = row['y']
            z = row['z']
            if minX <= x <= maxX and minY <= y <= maxY and minZ <= z <= maxZ:
                is_within_boundaries.append(True)
            else:
                is_within_boundaries.append(False)
        return is_within_boundaries
    
    def player_weapon_classes(self):
        weapon_classes = []
        for i, row in self.df.iterrows():
            inventory = row['inventory']
            if inventory is not None:
                for el in inventory:
                    weapon_class = el['weapon_class']
                    if weapon_class not in weapon_classes:
                        weapon_classes.append(weapon_class)

        return weapon_classes





def main():
    gameState = ProcessGameState("game_state_frame_data.parquet")
    gameState.ingest_file()

    #question 2.a.:
    boundaries = [-2805,-1565, 250, 1233, 285, 421]
    team2_T_data = gameState.get_team_side_data('Team2', 'T')
    players = gameState.check_player_boundaries(team2_T_data, boundaries)
    percentage_entering = sum(players)/len(players)*100
    print(percentage_entering)
    print(f'based on the results obtained {percentage_entering:.2f}% of the T side Team2 players enter the light blue boundary. So it is not a common strategy that they use.')
    #question 3.a.:
    
main()