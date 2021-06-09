from heapq import heappush, heappop

def astar_shortest_path(src, isdst, adj, heuristic):
    dist = {}
    dist_no_heur = {}
    prev = {}
    dist[src] = 0.0
    dist_no_heur[src] = 0.0
    prev[src] = None
    heap = [(dist[src], src,0)]

    pathLength = float('inf')
    while heap:
        node = heappop(heap)
        if isdst(node[1]):
            path = []
            nodeR = node[1]
            while nodeR:
                path.append([nodeR, dist_no_heur[nodeR]])
                nodeR = prev[nodeR]
            path.reverse()
            for ii in xrange(len(path) - 1, 0, -1):
                path[ii][1] -= path[ii - 1][1]
            return path

        for next_node in adj(node):
            next_node[0] += heuristic(next_node[1])
            next_node.append(heuristic(next_node[1]))
            if next_node[1] not in dist or next_node[0] < dist[next_node[1]]:
                #print node[1],next_node[1],heuristic(next_node[1])
                #exit()

                dist[next_node[1]] = next_node[0]
                dist_no_heur[next_node[1]] = next_node[0] - next_node[2]
                prev[next_node[1]] = node[1]
                heappush(heap, next_node)

    return None

MOD_COST = 1000

GAME_SMB = 'SMB_mod'
GAME_KI = 'KI_mod'
GAME_DNG = 'DNG_mod'

GAMES = [GAME_SMB, GAME_KI, GAME_DNG]
GAME_IS = None

def makeIsSolid(solids):
    def isSolid(tile):
        return tile in solids
    return isSolid

def makeGetNeighbors(jumps,levelStr,cant_mod,visited,isSolid,mod_allow):
    maxX = len(levelStr[0])-1
    maxY = len(levelStr)-1
    jumpDiffs = []
    for jump in jumps:
        jumpDiff = [jump[0]]
        for ii in range(1,len(jump)):
            jumpDiff.append((jump[ii][0]-jump[ii-1][0],jump[ii][1]-jump[ii-1][1]))
        jumpDiffs.append(jumpDiff)
    jumps = jumpDiffs
    def getNeighbors(pos):
        dist = pos[0]-pos[2]
        pos = pos[1]
        visited.add((pos[0],pos[1]))
        below = (pos[0],pos[1]+1)
        neighbors = []

        if GAME_IS == GAME_DNG:
            for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                #nx, ny = (pos[0] + dx + maxX+1) % (maxX+1), (pos[1] + dy + maxY+1) % (maxY+1)
                nx, ny = pos[0] + dx, pos[1] + dy
                if nx < 1 or nx > maxX-1 or ny < 1 or ny > maxY-1:
                    continue

                if not isSolid(levelStr[ny][nx]):
                    neighbors.append([dist+1,(nx, ny, -1)])
    
                if isSolid(levelStr[ny][nx]):
                    if mod_allow and (nx,ny) not in cant_mod:
                        import random
                        random.seed(11 * nx + 17 * ny)
                        mod_cost_dng = MOD_COST * random.randint(1, 10) ** 2
                        neighbors.append([dist+1+mod_cost_dng,(nx, ny, -1)])
            return neighbors
        
        if below[1] > maxY:
            return []
        if pos[2] != -1:
            ii = pos[3] +1
            jump = pos[2]
            if ii < len(jumps[jump]):
                nx, ny = pos[0]+pos[4]*jumps[jump][ii][0], pos[1]+jumps[jump][ii][1]

                if not (nx > maxX or nx < 0 or ny < 0) and not isSolid(levelStr[ny][nx]):
                    neighbors.append([dist+1,(nx,ny,jump,ii,pos[4])])
                #if ny < 0 and not isSolid(levelStr[ny][nx]):
                #    neighbors.append([dist+1,(nx,0,jump,ii,pos[4])])

                if not (nx > maxX or nx < 0 or ny < 0) and isSolid(levelStr[ny][nx]):
                    if mod_allow and (nx,ny) not in cant_mod:
                        neighbors.append([dist+1+MOD_COST,(nx,ny,jump,ii,pos[4])])
                #if ny < 0 and isSolid(levelStr[ny][nx]):
                #    if mod_allow and (nx,0) not in cant_mod:
                #        neighbors.append([dist+1+MOD_COST,(nx,0,jump,ii,pos[4])])

        if GAME_IS == GAME_KI:
            if pos[0]+1 == maxX + 1:
                new_pos = (0,) + pos[1:]
                if not isSolid(levelStr[pos[1]][0]):
                    neighbors.append([dist+1,new_pos])
            if pos[0]-1 == -1:
                new_pos = (maxX,) + pos[1:]
                if not isSolid(levelStr[pos[1]][maxX]):
                    neighbors.append([dist+1,new_pos])

        if isSolid(levelStr[below[1]][below[0]]):
            if (not mod_allow) or (below not in visited):
                if pos[0]+1 <= maxX and not isSolid(levelStr[pos[1]][pos[0]+1]):
                    neighbors.append([dist+1,(pos[0]+1,pos[1],-1)])
                if pos[0]-1 >= 0 and not isSolid(levelStr[pos[1]][pos[0]-1]):
                    neighbors.append([dist+1,(pos[0]-1,pos[1],-1)])

                if pos[0]+1 <= maxX and isSolid(levelStr[pos[1]][pos[0]+1]):
                    if mod_allow and (pos[0]+1,pos[1]) not in cant_mod:
                        neighbors.append([dist+1+MOD_COST,(pos[0]+1,pos[1],-1)])
                if pos[0]-1 >= 0 and isSolid(levelStr[pos[1]][pos[0]-1]):
                    if mod_allow and (pos[0]-1,pos[1]) not in cant_mod:
                        neighbors.append([dist+1+MOD_COST,(pos[0]-1,pos[1],-1)])

                for jump in range(len(jumps)):
                    ii = 0
                    nxl, nxr, ny = pos[0]-jumps[jump][ii][0], pos[0]+jumps[jump][ii][0], pos[1]+jumps[jump][ii][1]

                    if ny < 0:
                        continue

                    if not (nxr > maxX or pos[1] < 0) and not isSolid(levelStr[ny][nxr]):
                        neighbors.append([dist+ii+1,(nxr,ny,jump,ii,1)])
                    if not (nxl < 0 or pos[1] < 0) and not isSolid(levelStr[ny][nxl]):
                        neighbors.append([dist+ii+1,(nxl,ny,jump,ii,-1)])

                    if not (nxr > maxX or pos[1] < 0) and isSolid(levelStr[ny][nxr]):
                        if mod_allow and (nxr,ny) not in cant_mod:
                            neighbors.append([dist+ii+1+MOD_COST,(nxr,ny,jump,ii,1)])
                    if not (nxl < 0 or pos[1] < 0) and isSolid(levelStr[ny][nxl]):
                        if mod_allow and (nxl,ny) not in cant_mod:
                            neighbors.append([dist+ii+1+MOD_COST,(nxl,ny,jump,ii,-1)])

        else:
            neighbors.append([dist+1,(pos[0],pos[1]+1,-1)])
            if pos[1]+1 <= maxY:
                if pos[0]+1 <= maxX:
                    if not isSolid(levelStr[pos[1]+1][pos[0]+1]):
                        neighbors.append([dist+1.4,(pos[0]+1,pos[1]+1,-1)])
                    if isSolid(levelStr[pos[1]+1][pos[0]+1]):
                        if mod_allow and (pos[0]+1, pos[1]+1) not in cant_mod:
                            neighbors.append([dist+1.4+MOD_COST,(pos[0]+1,pos[1]+1,-1)])
                
                if pos[0]-1 >= 0:
                    if not isSolid(levelStr[pos[1]+1][pos[0]-1]):
                        neighbors.append([dist+1.4,(pos[0]-1,pos[1]+1,-1)])
                    if isSolid(levelStr[pos[1]+1][pos[0]-1]):
                        if mod_allow and (pos[0]-1, pos[1]+1) not in cant_mod:
                            neighbors.append([dist+1.4+MOD_COST,(pos[0]-1,pos[1]+1,-1)])

            if mod_allow and below not in visited and below not in cant_mod:
                for jump in range(len(jumps)):
                    ii = 0
                    nxl, nxr, ny = pos[0]-jumps[jump][ii][0], pos[0]+jumps[jump][ii][0], pos[1]+jumps[jump][ii][1]

                    if ny < 0:
                        continue

                    if not (nxr > maxX or pos[1] < 0) and not isSolid(levelStr[ny][nxr]):
                        if mod_allow and below not in cant_mod:
                            neighbors.append([dist+ii+1+MOD_COST,(nxr,ny,jump,ii,1)])
                    if not (nxl < 0 or pos[1] < 0) and not isSolid(levelStr[ny][nxl]):
                        if mod_allow and below not in cant_mod:
                            neighbors.append([dist+ii+1+MOD_COST,(nxl,ny,jump,ii,-1)])

                    # TODO: add isSolid versions ?

        return neighbors
    return getNeighbors

def searchParams(isSolid,levelStr):
    maxY = len(levelStr)-1
    maxX = len(levelStr[0])-1

    startX, startY, goalX, goalY = None, None, None, None

    for ri, r in enumerate(levelStr):
        for ci, c in enumerate(r):
            if c == '{':
                startX, startY = ci, ri
            if c == '}':
                goalX, goalY = ci, ri

    if startX == None or startY == None:
        raise RuntimeError("level has no start")
    if goalX == None or goalY == None:
        raise RuntimeError("level has no goal")
    
    return maxX, maxY, startX, startY, goalX, goalY



def confirmPath(isSolid,jumps,levelStr,params,path):
    maxX, maxY, startX, startY, goalX, goalY = params

    if path[0][0][0] != startX or path[0][0][1] != startY:
        return False
    if path[-1][0][0] != goalX or path[-1][0][1] != goalY:
        return False

    visited = set()
    cant_mod = set()
    getNeighbors = makeGetNeighbors(jumps,levelStr,cant_mod,visited,isSolid,False)

    for pi in range(len(path)-1):
        neighbors = getNeighbors((0, path[pi][0], 0))
        neighbors = [n[1] for n in neighbors]
        if path[pi + 1][0] not in neighbors:
            return False

    return True



def findPaths(isSolid,jumps,mod_allow,levelStr,params):
    maxX, maxY, startX, startY, goalX, goalY = params

    visited = set()
    cant_mod = set()
    getNeighbors = makeGetNeighbors(jumps,levelStr,cant_mod,visited,isSolid,mod_allow)

    # this prevents the level from being modded in such a way that moves the start or goal
    cant_mod.add((startX, startY))
    cant_mod.add((goalX, goalY))
    if GAME_IS in [GAME_KI, GAME_SMB]:
        cant_mod.add((startX, startY+1))
        cant_mod.add((goalX, goalY+1))

    path = astar_shortest_path((startX,startY,-1), lambda pos: pos[0] == goalX and pos[1] == goalY, getNeighbors, lambda pos: 0)
    #lambda pos: ((goalX - pos[0]) ** 2 + (goalY - pos[1]) ** 2) ** 0.5) # TODO: ?? account for KI wrap
    #path = pathfinding_mod.astar_shortest_path( (2,2,-1), lambda pos: pos[0] == maxX, getNeighbors, lambda pos: 0)#lambda pos: abs(maxX-pos[0]))

    return path



if __name__ == "__main__":
    import argparse
    import sys
    import json

    parser = argparse.ArgumentParser(description='Level pathfinding.')
    parser.add_argument('descriptionfile', type=str, help='Platformer description file.')
    parser.add_argument('levelfile', type=str, help='Level file.')
    parser.add_argument('--modify', action='store_true', help='Can modify level.')
    args = parser.parse_args()

    GAME_IS = args.descriptionfile.split('.')[0]
    if GAME_IS not in GAMES:
        sys.stderr.write('Unreconized description file: %s.\n' % GAME_IS)
        sys.exit(-1)

    sys.stderr.write('Using %s rules...\n' % GAME_IS)

    mod_allow = args.modify
    
    levelFilename = args.levelfile
    level = []
    with open(levelFilename) as level_file:
        for line in level_file:
            level.append(line.rstrip())
    with open(args.descriptionfile) as data_file:    
        platformerDescription = json.load(data_file)

    isSolid = makeIsSolid(platformerDescription['solid'])
    jumps = platformerDescription['jumps']

    params = searchParams(isSolid,level)
    maxX, maxY, startX, startY, goalX, goalY = params

    path = findPaths(isSolid,jumps,mod_allow,level, params)

    if not path:
        sys.stderr.write('No path found.\n')
        sys.exit(0)

    on_path = set()
    mod_from_solid = set()
    mod_to_solid = set()

    # find modifications
    for pi, (pos, dist) in enumerate(path):
        px, py, pj = pos[0], pos[1], pos[2]

        on_path.add((px, py))

        if mod_allow:
            is_mod_dist = dist >= MOD_COST
            is_mod_from_solid = None
            is_mod_to_solid = None

            if isSolid(level[py][px]):
                is_mod_from_solid = (px, py)

            if GAME_IS in [GAME_SMB, GAME_KI]:
                if pj != -1 and pi > 0:
                    pjii = pos[3]
                    prev_pos = path[pi - 1][0]
                    prev_px, prev_py = prev_pos[0], prev_pos[1]
                    if pjii == 0 and not isSolid(level[prev_py+1][prev_px]):
                        if not(GAME_IS == GAME_KI and abs(px - prev_px) > 1): #if in KI and wrapped, mod should have been handled prior to wrap
                            is_mod_to_solid = (prev_px, prev_py+1)

            if is_mod_dist and not (is_mod_from_solid or is_mod_to_solid):
                raise RuntimeError("has mod dist but no mod found")

            if not is_mod_dist and (is_mod_from_solid or is_mod_to_solid):
                raise RuntimeError("mod found but not mod dist")

            if is_mod_from_solid and is_mod_to_solid:
                raise RuntimeError("found mod from and mod to solid")

            if is_mod_from_solid:
                mod_from_solid.add(is_mod_from_solid)
            if is_mod_to_solid:
                mod_to_solid.add(is_mod_to_solid)
            
    if not mod_from_solid.isdisjoint(mod_to_solid):
        raise RuntimeError("tile mod to and from solid")

    if (startX, startY) in mod_to_solid:
        raise RuntimeError("start mod to solid")
    if (goalX, goalY) in mod_to_solid:
        raise RuntimeError("goal mod to solid")
    if (startX, startY) in mod_from_solid:
        raise RuntimeError("start mod from solid")
    if (goalX, goalY) in mod_from_solid:
        raise RuntimeError("goal mod from solid")

    # confirm path
    if mod_allow:
        modded_level = [list(row) for row in level]

        for (x, y) in mod_from_solid:
            modded_level[y][x] = '-'
        for (x, y) in mod_to_solid:
            modded_level[y][x] = platformerDescription['solid'][0]
        
        confirmed = confirmPath(isSolid,jumps,modded_level,params,path)
        if not confirmed:
            sys.stderr.write('Path found but not confirmed.\n')
            sys.exit(0)

    # # print
    # for ri, r in enumerate(level):
    #     rs = ''
    #     for ci, c in enumerate(r):
    #         if (ci, ri) in mod_from_solid:
    #             rs += '+'
    #         elif (ci, ri) in mod_to_solid:
    #             rs += '^'
    #         elif (ci, ri) == (startX, startY):
    #             rs += '{'
    #         elif (ci, ri) == (goalX, goalY):
    #             rs += '}'
    #         elif (ci, ri) in on_path:
    #             rs += '.'
    #         else:
    #             rs += c
    #     print(rs)
    # print()

    # # check no shortcuts
    # for pi in range(1, len(path)):
    #     px, py = path[pi][0][0], path[pi][0][1]
    #     ppx, ppy = path[pi - 1][0][0], path[pi - 1][0][1]

    #     x0, x1 = min(px, ppx), max(px, ppx)
    #     y0, y1 = min(py, ppy), max(py, ppy)

    #     if GAME_IS == GAME_DNG:
    #         if abs(x0 - x1) > 1 and (not x0 == 0 and x1 == maxX):
    #             raise RuntimeError("shortcut: moved too far!")
    #         if abs(y0 - y1) > 1 and (not y0 == 0 and y1 == maxY):
    #             raise RuntimeError("shortcut: moved too far!")
    #     else:
    #         if GAME_IS == GAME_KI:
    #             if abs(x0 - x1) > 1 and (not x0 == 0 and x1 == maxX):
    #                 raise RuntimeError("shortcut: moved too far!")
    #         else:
    #             if abs(x0 - x1) > 1:
    #                 raise RuntimeError("shortcut: moved too far!")
    #         if abs(y0 - y1) > 1:
    #             raise RuntimeError("shortcut: moved too far!")

    #     if x0 < x1:
    #         if y0 < y1:
    #             if isSolid(level[y0+1][x0]) and isSolid(level[y0][(x0+1)%maxX]):
    #                 raise RuntimeError("shortcut: diagonal 1!")
    #         if y1 < y0:
    #             if isSolid(level[y0-1][x0]) and isSolid(level[y0][(x0+1)%maxX]):
    #                 raise RuntimeError("shortcut: diagonal 2!")
