import pandas as pd
import pyarrow
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt

class ProcessGameState:


    def __init__(self, file_path) -> None:
        self.file_path = file_path
        self.df = pd.DataFrame()

    def ingest_file(self):
        self.df = pd.read_parquet(self.file_path)

    #returns a table containing players information for a specific team and side
    def get_team_side_data(self, team, side):
        return self.df[(self.df['team'] == team) & (self.df['side'] == side)]

    #checks whether a player is within the boundaries provided
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
    
    #returns the weapon classes used in the game
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
    
    #returns the weapon classes used by a specific player
    def player_index_weapon_classes(self, index):
        weapon_classes = []
        inventory = self.df.at[index, 'inventory']
        if inventory is not None:
                for el in inventory:
                    weapon_class = el['weapon_class']
                    if weapon_class not in weapon_classes:
                        weapon_classes.append(weapon_class)
        
        return weapon_classes

    #calculates the average timer, for question 2.b
    #My strategy for this question was getting the information for team2, T, checking if each one is in the boundaries, if they are, then I check their inventory and increment 
    #the count if there are atleast 2 smgs or rifles in total, to find the average for the concatenated timer. 
    def calculate_avg_timer(self, team, side, boundaries):
        data = self.get_team_side_data(team, side)
        isInBomb = self.check_player_boundaries(data,boundaries)
        count = 0
        timer_sum = 0
        weapons_list = []
        for i in range(len(isInBomb)):
            if isInBomb[i]:
                weapons = self.player_index_weapon_classes(i)
                for el in weapons: 
                    if el == 'Rifle' or el == 'SMG':
                        weapons_list.append(el)
                if len(weapons_list) >= 2:
                    timer = self.df.at[i,'clock_time']
                    timer_sum = timer_sum + self.convert_timer_to_s(timer)
                    count +=1
        avg_timer = None
        if count > 0:
            avg_timer = timer_sum/count
        return self.convert_s_to_timer(avg_timer)
    
    def convert_timer_to_s(self, timer):
        m, s = timer.split(':')
        total_s = int(m)*60+int(s)
        return total_s
    
    def convert_s_to_timer(self, s):
        minutes = int(s//60)
        seconds = int(s%60)
        return f"{minutes:02d}:{seconds:02d}"

    #generates a heatmap, for question 2.c
    def CT_heatmap(self, boundaries):
        ct = self.get_team_side_data('Team2', 'CT')
        is_in_bomb = self.check_player_boundaries(ct, boundaries)
        heatmap_data = np.zeros((1233,2805))
        for i in range(len(is_in_bomb)):
            if is_in_bomb[i]:
                row = ct.iloc[i]['y']
                col = ct.iloc[i]['x']
                heatmap_data[row, col] += 1

        sns.heatmap(heatmap_data, cmap='Blues', annot=True, fmt='g')
        plt.xlabel('X Coordinate')
        plt.ylabel('Y Coordinate')
        plt.title('CT Player Positions in B')
        plt.show()






def main():
    gameState = ProcessGameState("game_state_frame_data.parquet")
    gameState.ingest_file()

    print("question 2.a:")
    #the boundaries array is of length 6, and contains minX, maxX, minY, maxY, minZ, and maxZ respectively.
    boundaries_blue = [-2805,-1565, 250, 1233, 285, 421]
    team2_T_data = gameState.get_team_side_data('Team2', 'T')
    players = gameState.check_player_boundaries(team2_T_data, boundaries_blue)
    percentage_entering = sum(players)/len(players)*100
    print(percentage_entering)
    print(f'based on the results obtained {percentage_entering:.2f}% of the T side Team2 players enter the light blue boundary. So it is not a common strategy that they use.')

    print()
    print("question 2.b:")
    boundaries_B = [-2806,9999, 0, 1233, 285, 421]
    avg_timer = gameState.calculate_avg_timer('Team2','T',boundaries_B)
    print(f'The average timer where the team2 T side enters B with atleast 2 rifles or SMGs is: {avg_timer}')

    print()
    print("question 2.c:")
    #gameState.CT_heatmap(boundaries_B)
    print("""I am having technical issues with my work laptop trying to generate the heatmap, but it should work on a more powerful computer. My strategy for this step was basically
    filtering the CT team2 side, checking which ones are inside the bomb, and creating the heatmap with their coordinates.""")

    
main()