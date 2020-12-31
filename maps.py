import skills
import heroes
import dijkstra
import time
import os

### Drawing the Map
### Coordinates
### 0 - Map Border
### 1 - wall
### 2 - wall (1 hit)
### 3 - wall (2 hit)
### 4 - floor
### 5 - defensive
### 6 - trenches
### 7 - trenches defensive (?)
### 8 - forest
### 9 - forest defensive
### 10 - mountain/water (flier only)


def setMap(map, difficulty):   # type: "map" or "enemies"
    # Story Maps
    if map == "The Rite of Blades" and difficulty == "Lunatic":
        return [
            [[0, "0"], [0, "0"], [0, "0"], [0, "0"], [0, "0"], [0, "0"], [0, "0"], [0, "0"]],
            [[0, "0"], [4, "0"], [4, "0"], [4, "a"], [4, "0"], [4, "0"], [4, "0"], [0, "0"]],
            [[0, "0"], [4, "b"], [4, "0"], [4, "c"], [4, "d"], [4, "e"], [4, "0"], [0, "0"]],
            [[0, "0"], [4, "0"], [1, "0"], [4, "0"], [4, "0"], [1, "0"], [4, "0"], [0, "0"]],
            [[0, "0"], [4, "0"], [4, "0"], [4, "0"], [2, "0"], [4, "0"], [4, "0"], [0, "0"]],
            [[0, "0"], [4, "0"], [4, "0"], [4, "0"], [4, "0"], [4, "0"], [1, "0"], [0, "0"]],
            [[0, "0"], [1, "0"], [4, "1"], [1, "0"], [4, "2"], [4, "3"], [4, "0"], [0, "0"]],
            [[0, "0"], [4, "0"], [4, "4"], [4, "0"], [4, "0"], [4, "0"], [1, "0"], [0, "0"]],
            [[0, "0"], [4, "0"], [4, "0"], [4, "0"], [4, "0"], [4, "0"], [4, "0"], [0, "0"]],
            [[0, "0"], [0, "0"], [0, "0"], [0, "0"], [0, "0"], [0, "0"], [0, "0"], [0, "0"]]]

  
def setEnemies(map, difficulty, index):
    # Story Maps
    if map == "The Rite of Blades" and difficulty == "Lunatic":
        if index == "a":
            return "Eliwood", 39, 31, 30, 24, 32, "Blazing Durandal", "None", "Sacred Cowl", "None", "Axebreaker 3", "Drive Res 2", "None", "None", 1
        elif index == "b":
            return "Merric", 43, 27, 32, 28, 19, "Dark Excalibur", "None", "Growing Wind", "HP +5", "None", "Spur Res 3", "None", "None", 2
        elif index == "c":
            return "Linde", 36, 36, 37, 15, 27, "Dark Aura", "Ardent Sacrifice", "None", "Speed +3", "None", "Fortify Res 3", "None", "None", 3
        elif index == "d":
            return "Seliph", 48, 35, 25, 30, 23, "Divine Tyrfing", "Rally Speed", "None", "HP +5", "Brash Assault 3", "None", "None", "None", 4
        elif index == "e":
            return "Julia", 38, 36, 27, 17, 32, "Divine Naga", "None", "Dragon Fang", "Resistance +3", "None", "Breath of Life 3", "None", "None", 5
        else: return None


def getEnemyCount(map, difficulty):
    #Story Maps
    if map == "The Rite of Blades" and difficulty == "Lunatic":
        return 5