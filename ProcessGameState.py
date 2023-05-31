import pandas as pd
import seaborn as sns
import numpy as np
import matplotlib.pyplot as plt

class ProcessGameStrategy:
    def withinBound(filename, x1, y1, x2, y2, maxz, minz, team, side):
        
        #Converts File to DataFrame
        df = pd.read_parquet(filename, engine='auto')

        #Vairables for iteration purposes
        axes = ["x","y","z"]
        count = 0
        currentx = 0
        currenty = 0
        currentz = 0
        x = []
        y = []
        z = []
        round = []
        
        #Since inputs given as corners or a boundary, determines higher/lower x and ys for boundary
        if(x1>x2):
            maxx = x1
            minx = x2
        else:
            maxx = x2
            minx = x1
        if(y1>y2):
            maxy = y1
            miny = y2
        else:
            maxy = y2
            miny = y1

        #For loop to iterate through columns x, y, and z of the DataFrame
        for point, row in df.iterrows():
            #print(df.at[point,"side"])
            if((df.at[point,"side"]==side) and (df.at[point,"team"] == team)):
                for axis in axes:
                    #Checks if each point is within its boundary 
                    if(axis == "x"):
                        if((row[axis]>=minx) and (row[axis]<=maxx)):
                            count = count + 1
                            currentx = row[axis]
                    elif (axis == "y"):
                        if((row[axis]>=miny) and (row[axis]<=maxy)):
                            count = count + 1
                            currenty = row[axis]
                    else:
                        if((row[axis]>=minz) and (row[axis]<=maxz)):
                            count = count + 1
                            currentz = row[axis]
            #If all three points are within the boundary add the entire point 
            if(count==3):
                x.append(currentx)
                y.append(currenty)
                z.append(currentz)  
                round.append(df.at[point,"round_num"])
            count = 0    

        #Creates the return DataFrame for all the points that met the boundary requirements 
        Points = pd.DataFrame(data=x, columns=["x"])
        Points['y'] = y
        Points['z'] = z
        Points['round'] = round
        return Points
   
    def getInventory(filename, team, side):
        #Converts File to DataFrame
        df = pd.read_parquet(filename, engine='auto')
        
        #Vairables for iteration purposes
        weapon_classes = []
        round = []
        player = []
        
        #For loop to iterate through rows of the DataFrame
        for indices, row in df.iterrows():
            temp_weapon = []
            if((df.at[indices,"side"] == side) and (df.at[indices,"team"] == team)):
                inventory = df.at[indices,"inventory"]
                if(not(inventory is None)):
                    #For Loop to iterate through the list of dictionaries 
                    for x in inventory:
                        #Extracting weapon_class
                        temp_weapon.append(x["weapon_class"])
            
            #Cleaning Up Table format and Tracking Round Number and Player 
            if(len(temp_weapon)>1):
                weapons = " "
                for y in temp_weapon:
                   weapons = weapons + " " + y
                weapon_classes.append(weapons) 
                round.append(df.at[indices,"round_num"])
                player.append(df.at[indices,"player"])
            elif (len(temp_weapon) == 1):
                weapon_classes.append(temp_weapon[0])  
                round.append(df.at[indices,"round_num"])   
                player.append(df.at[indices,"player"])       
        
        #Creates the return DataFrame for all the weapons 
        weapons = pd.DataFrame(data=weapon_classes, columns=["weapon"])
        weapons['round'] = round
        weapons['player'] = player
        return(weapons)
    
    def averageTime(filename,team,side,min_gun,area_name):
        #Converts File to DataFrame
        df = pd.read_parquet(filename, engine='auto')

        #Vairables for iteration purposes
        times = []
        rounds = []
        players = []
        final_times = []
        count = 0

        for indices, row in df.iterrows():
            #Locating the time points of entry into BombsiteB
            if((df.at[indices,"side"] == side) and (df.at[indices,"team"] == team) and (df.at[indices,"area_name"] == area_name) and (df.at[indices, side.lower() + "_alive"] >=2) and (df.at[indices,"is_alive"] == True)):
                round = df.at[indices,"round_num"] 
                time = df.at[indices,"clock_time"]
                player = df.at[indices,"player"]
                
                #List of rounds and times of entry where at least two people are alive 
                if not(round in rounds):
                    times.append(time)
                    rounds.append(round)
                    players.append(player)
        print(times)       
        #Now we need to check what the alive players have in their inventory 
        inventory = ProcessGameStrategy.getInventory(filename, team, side)
        for x, row in inventory.iterrows():
            y = 0
            while y < len(players):
                #Checking for the gun requirements 
                if((rounds[y] == inventory.at[x,"round"]) and players[y] == inventory.at[x,"player"]):
                    if(("Rifle" in inventory.at[x,"weapon"]) or ("SMG" in inventory.at[x,"weapon"])): 
                        count += 1
                if (count >=2):
                    final_times.append(times[y])
                y = y+1
            count=0
        print(final_times)
#The following is just a sampel heatmap as I did not figure out the B site coordinates. 
    def mapPoints(filename,team,side):
        np.random.seed(0)
        sns.set()
        data = np.random.rand(10, 12)
        #data = ProcessGameStrategy.withinBound(parquet_file, B SITE COORDINATES AS INPUTS,"Team2","T")
        
        ax = sns.heatmap(data, vmin=0, vmax=1)
        plt.show()


parquet_file = 'game_state_frame_data.parquet'
#print(pd.read_parquet(parquet_file, engine='auto'))
print(ProcessGameStrategy.withinBound(parquet_file, -1735, 250,-2472, 1233, 421, 285,"Team2","T"))
print(ProcessGameStrategy.getInventory(parquet_file,"Team2","T"))

#Below is the unfinished function being used to fully output the answer to Question 2B
print(ProcessGameStrategy.averageTime(parquet_file,"Team2","T",2,"BombsiteB"))



