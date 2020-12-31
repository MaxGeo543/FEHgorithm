def dijkstra(map, start, goalx, goaly, a):                     # a defines what is returned 0=shortest distance 1=path
    ### creating compatible graph from map
    infinity = 99999999
    graph = {}
    y = 1
    while y <= 8:
        x = 1
        while x <= 6:
            adj = {}
            ### Create adj x+1
            if map[y][x+1][0] <= 3:
                pass
            elif map[y][x+1][0] <= 5:
                adj[(x+1, y)] = 1
            elif map[y][x+1][0] <= 7:
                if start.mvt_type == "cav": adj[(x+1, y)] = 3
                else: adj[(x+1, y)] = 1
            elif map[y][x+1][0] <= 9:
                if start.mvt_type == "inf": adj[(x+1, y)] = 2
                elif start.mvt_type == "cav": pass
                else: adj[(x+1, y)] = 1
            elif map[y][x+1][0] == 10:
                if start.mvt_type == "fly": adj[(x+1, y)] = 1
                else: pass
        
            ### Create adj x-1
            if map[y][x-1][0] <= 3:
                pass
            elif map[y][x-1][0] <= 5:
                adj[(x-1, y)] = 1
            elif map[y][x-1][0] <= 7:
                if start.mvt_type == "cav": adj[(x-1, y)] = 3
                else: adj[(x-1, y)] = 1
            elif map[y][x-1][0] <= 9:
                if start.mvt_type == "inf": adj[(x-1, y)] = 2
                elif start.mvt_type == "cav": pass
                else: adj[(x-1, y)] = 1
            elif map[y][x-1][0] == 10:
                if start.mvt_type == "fly": adj[(x-1, y)] = 1
                else: pass
            
            ### Create adj y+1
            if map[y+1][x][0] <= 3:
                pass
            elif map[y+1][x][0] <= 5:
                adj[(x, y+1)] = 1
            elif map[y+1][x][0] <= 7:
                if start.mvt_type == "cav": adj[(x, y+1)] = 3
                else: adj[(x, y+1)] = 1
            elif map[y+1][x][0] <= 9:
                if start.mvt_type == "inf": adj[(x, y+1)] = 2
                elif start.mvt_type == "cav": pass
                else: adj[(x, y+1)] = 1
            elif map[y+1][x][0] == 10:
                if start.mvt_type == "fly": adj[(x, y+1)] = 1
                else: pass
        
            ### Create adj y-1
            if map[y-1][x][0] <= 3:
                pass
            elif map[y-1][x][0] <= 5:
                adj[(x, y-1)] = 1
            elif map[y-1][x][0] <= 7:
                if start.mvt_type == "cav": adj[(x, y-1)] = 3
                else: adj[(x, y-1)] = 1
            elif map[y-1][x][0] <= 9:
                if start.mvt_type == "inf": adj[(x, y-1)] = 2
                elif start.mvt_type == "cav": pass
                else: adj[(x, y-1)] = 1
            elif map[y-1][x][0] == 10:
                if start.mvt_type == "fly": adj[(x, y-1)] = 1
                else: pass
        
            graph[(x, y)] = adj 
            x += 1
        y += 1
    
    ### actual dijkstra algorithm
    shortest_distance = {}
    track_predecessor = {}
    unseenTiles = graph
    track_path = []
    
    for tile in unseenTiles:
        shortest_distance[tile] = infinity                                                       # setting shortest distance to every tile to infinity
    shortest_distance[(start.x, start.y)] = 0                                                    # setting distance to start to 0
    
    while unseenTiles:
        min_distance_tile = None
        for tile in unseenTiles:
            if min_distance_tile == None:
                min_distance_tile = tile
            elif shortest_distance[tile] < shortest_distance[min_distance_tile]:                 # --> min_distance_tile = (start.x, start.y) (2, 6)
                min_distance_tile = tile
        
        path_options = graph[min_distance_tile].items()                                          # path_options of (start.x, start.y) = (1, 6):99999  (3, 6):99999   (2, 7):1 (2, 5):1
        
        for child_tile, weight in path_options:                                                  # child tile = adjacent tile ;;; weight = trenches/forest/floor etc.
            if weight + shortest_distance[min_distance_tile] < shortest_distance[child_tile]:    # 99 + 0 < 999999                                   
                shortest_distance[child_tile] = weight + shortest_distance[min_distance_tile]    # overwrite 999999 of childtile with weight of it
                track_predecessor[child_tile] = min_distance_tile
    
        unseenTiles.pop(min_distance_tile)                                                       # delete old min_distance_tile
    currentTile = (goalx, goaly)
    
    while currentTile != (start.x, start.y):
        try:
            track_path.insert(0, currentTile)
            currentTile = track_predecessor[currentTile]
        
        except KeyError:
            #print("No Path.")
            break
    
    track_path.insert(0, (start.x, start.y))
    
    if shortest_distance[goalx, goaly] != infinity:
        if a == 0: return shortest_distance[goalx, goaly] #=shortest distance
        elif a == 1: return track_path #=order of movements to achieve optimal distance
        else: 
            return 0
            print("Nothing Returned.")