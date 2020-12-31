import skills
import heroes
import maps
import dijkstra
import time
import os

MAPNAME = ("The Rite of Blades", "Lunatic")             #actual Name and difficulty
ALPHABET = ["a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m", "n", "o", "p", "q", "r", "s", "t", "u", "v", "w", "x", "y", "z"]

class Unit:
    players = []
    enemies = []
    
    def __init__(self, name, max_hp, base_atk, base_spd, base_def, base_res, weapon, assist, special, a_skill, b_skill, c_skill, seal, duo, slot, player):
        #player or enemy
        if player:
            Unit.players.append(self)
        else: Unit.enemies.append(self)
        
        #stats
        self.max_hp = max_hp     #hp
        self.base_atk = base_atk #atk
        self.base_spd = base_spd #spd
        self.base_def = base_def #de
        self.base_res = base_res #res
        
        #equipment
        self.weapon = weapon     #wpn
        self.assist = assist     #ass
        self.special = special   #spc
        self.a_skill = a_skill   #a
        self.b_skill = b_skill   #b
        self.c_skill = c_skill   #c
        self.seal = seal         #s
        self.duo = duo
        
        #hero specifics: color - weapon type - weapon range - movement type
        self.name = name
        self.color = heroes.stat[name][0]         #col
        self.weapon_type = heroes.stat[name][1]   #wpn_type
        if self.weapon_type == "staff" or self.weapon_type == "bow" or self.weapon_type == "dagger" or self.weapon_type == "tome":
            self.weapon_range = 2                 #wpn_rng
        else: self.weapon_range = 1
        self.movement_type = heroes.stat[name][2] #mvt_type
        
        #others
        self.slot = slot
        
        #in-battle variables
        self.current_hp = max_hp                  #c_hp
        self.visible_atk = 0                      #b_atk
        self.visible_spd = 0                      #b_spd
        self.visible_def = 0                      #b_de
        self.visible_res = 0                      #b_res
        self.pass_status = False                  #s_pass
        if self.movement_type == "arm":
            self.movement = 1                     #mvt
        elif self.movement_type == "cav":
            self.movement = 3
        else: self.movement = 2
        self.movement_bonus = 0
        self.movement_turn = 0
        
        #pre-defining position
        self.x = 0
        self.y = 0
        
        
    def stats(self):
        print(f'''
HP: {self.hp}
Atk: {self.base_atk}
Spd: {self.base_spd}
Def: {self.base_def}
Res: {self.base_res}
Rating: {self.max_hp + self.base_atk + self.base_spd + self.base_de + self.base_res}
''')


def turn(phase):
    if phase == "player":
        # Evaluate and store turn-wide states
        ## Evaluate and perform obstacle related processes
        ### granting pass status
        for unit in Unit.players+Unit.enemies:
            skills.effect(unit, "turn")

        ### Ally Obstacle List (used by enemies), storing the location of all tiles that are occupied by allies 
        allyObstacleList = []
        for player in Unit.players: allyObstacleList.append((player.x, player.y))

        ### Enemy Obstacle List (used by allies), storing the location of all tiles that are occupied by enemies 
        enemyObstacleList = []
        for enemy in Unit.enemies: enemyObstacleList.append((enemy.x, enemy.y))
        
        ### Block Obstacle List (used by both sides), storing the location of all tiles that have blocks (e.g. Walls)
        global blockObstacleList
        blockObstacleList = []
        y = 0
        while y < len(map):
            x = 0
            while x < len(map[0]):
                if map[y][x][0] == 1 or map[y][x][0] == 2 or map[y][x][0] == 3:
                   blockObstacleList.append((x, y))
                x += 1
            y += 1


        ## create Movement Order List
        global movementOrderList
        movementOrderList = []
        tieBreakerList = []
        orderDict = {}
        
        ### preparation
        distanceDict = {}
        for player in Unit.players:
            # distance to closest enemy
            allDistance = []
            for enemy in Unit.enemies:
                allDistance.append(dijkstra.dijkstra(map, player, enemy.x, enemy.y, 0))
            if not min(allDistance) in distanceDict:
                distanceDict[min(allDistance)] = []
            distanceDict[min(allDistance)].append(player)
        
        ### tiebreaker
        for player in Unit.players:
            tieBreaker = 0
            
            
            #### Assist N > Y
            if player.assist == "None": tieBreaker += 0
            else: tieBreaker += 267
            
            
            #### Attack Type Melee > Ranged > Weaponless
            if player.weapon == "None": tieBreaker += 266
            elif player.weapon_range == 2: tieBreaker += 133
            else: tieBreaker += 0
            
            
            #### valuating distance from allShortestDistance (lowest > highest)
            allShortestDistance = []
            for distance in distanceDict: allShortestDistance.append(distance)
            allShortestDistance.sort()
            for distance in allShortestDistance: 
                for unit in distanceDict[distance]:
                    if player == unit:
                        tieBreaker += allShortestDistance.index(distance)*12
            
            
            #### Slot lowest > highest
            tieBreaker += player.slot - 1
            
            
            #### updating orderDict and tieBreakerList
            orderDict[tieBreaker] = player
            tieBreakerList.append(tieBreaker)

        ### create Movement Order List
        tieBreakerList.sort()
        for i in tieBreakerList:
            movementOrderList.append(orderDict[i])


        ## store movement range of each unit
        global movementRange
        global threatRange
        movementRange = {}
        threatRange = {}
        for player in Unit.players:
            player.movement_turn = player.movement + player.movement_bonus
            movementRange[player] = list()
            threatRange[player] = list()
            y = 0
            while y < len(map):
                x = 0
                while x < len(map[0]):
                    try:
                        if dijkstra.dijkstra(map, player, x, y, 0) <= player.movement_turn:
                            movementRange[player].append((x, y))
                    except TypeError:
                        pass
                    except KeyError:
                        pass
                    x += 1
                y += 1
             
        # Assess Threats
            for tile in movementRange[player]:
                for i in range(player.weapon_range):
                    if not ((tile[0]+player.weapon_range-i, tile[1]+i) in threatRange[player]):
                        threatRange[player].append((tile[0]+player.weapon_range-i, tile[1]+i))
                    if not ((tile[0]-(player.weapon_range+i), tile[1]-i) in threatRange[player]):
                        threatRange[player].append((tile[0]-(player.weapon_range+i), tile[1]-i))
                    if not ((tile[0]+i, tile[1]-(player.weapon_range+i)) in threatRange[player]):
                        threatRange[player].append((tile[0]+i, tile[1]-(player.weapon_range+i)))
                    if not ((tile[0]-i, tile[1]+player.weapon_range-i) in threatRange[player]):
                        threatRange[player].append((tile[0]-i, tile[1]+player.weapon_range-i))
        

    

### Some side notes: 
### Maps are 6x8
### I use Intermission 1 (Rite of Blades) on lunatic as test map, thats the last map in Book I; next step is programming the map to be playable (no AIs yet)
###
### Building a Unit:'varname' = Unit(name, hp, atk, spd, def, res, weapon, assist, special, a-skill, b-skill, c-ckill, seal, slot number)
### name implies the heroe's name -> for all hero names look at heroes.py
### 'varname' could for example be: player_1; player_2; player_3; enemy_1; etc.





### Intermission I; Sample


### Pre-battle
### Defining Units. Naming: player's = p_(number) / enemy's: e_(letter)
playerDict = {}
playerDict[1] = Unit("Itsuki", 48, 42, 34, 34, 33, "Mirage Falchion", "Swap", "Aether", "Distant Counter", "Wrath 3", "Odd Atk Wave 3", "Heavy Blade 3", "None", 1, True)
playerDict[2] = Unit("Norne", 43, 32, 38, 30, 29, "Spendthrift Bow+ (+Res)", "Reposition", "Moonbow", "Distant Def 4", "Quick Riposte 3", "Threaten Def 3", "Distant Def 3", "None", 2, True)
playerDict[3] = Unit("Y!Minerva", 40, 33, 37, 36, 17, "Dragoon Axe", "Reposition", "Draconic Aura", "Dragoon Shield", "Flier Formation", "Atk/Def Oath 3", "None", "None", 3, True)
playerDict[4] = Unit("Reinhardt", 38, 32, 22, 25, 30, "Dire Thunder", "Reposition", "Moonbow", "Death Blow 4", "Vantage 3", "Goad Cavalry", "None", "None", 4, True)

enemyDict = {}
for e in range(0, maps.getEnemyCount(*MAPNAME)-1):
    enemyDict[ALPHABET[e]] = Unit(*maps.setEnemies(*MAPNAME, ALPHABET[e]), False)
map = maps.setMap(*MAPNAME)

### set x and y coordinates of all players and enemies
y = 0
while y < len(map):
    x = 0
    while x < len(map[0]):
        for player in Unit.players:
            if map[y][x][1] == str(Unit.players.index(player)+1):
                player.x = x
                player.y = y
        for enemy in Unit.enemies:
            if map[y][x][1] == ALPHABET[Unit.enemies.index(enemy)]:
                enemy.x = x
                enemy.y = y
        x += 1
    y += 1



### Battle
### applying permanent battle effects
for unit in Unit.players+Unit.enemies:
    skills.effect(unit, "permanent")

turn("player")

for i in movementOrderList:
    print(i.name)
    try:
        print(movementRange[i])
    except KeyError:
        print(i.name)
print(threatRange[movementOrderList[1]])
print(len(threatRange[movementOrderList[1]]))