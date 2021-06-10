from heapq import heappush, heappop

MOD_COST = 1000


def astar_shortest_path(src, isdst, adj, heuristic):
    dist = {}
    dist_no_heur = {}
    prev = {}
    dist[src] = 0.0
    dist_no_heur[src] = 0.0
    prev[src] = None
    heap = [(dist[src], src,0)]

    while heap:
        node = heappop(heap)
        if isdst(node[1]):
            path = []
            nodeR = node[1]
            while nodeR:
                path.append([nodeR, dist_no_heur[nodeR]])
                nodeR = prev[nodeR]
            path.reverse()
            for ii in range(len(path) - 1, 0, -1):
                path[ii][1] -= path[ii - 1][1]
            return path

        for next_node in adj(node):
            next_node[0] += heuristic(next_node[1])
            next_node.append(heuristic(next_node[1]))
            if next_node[1] not in dist or next_node[0] < dist[next_node[1]]:
                dist[next_node[1]] = next_node[0]
                dist_no_heur[next_node[1]] = next_node[0] - next_node[2]
                prev[next_node[1]] = node[1]
                heappush(heap, next_node)

    return None



def makeIsSolid(solids):
    def isSolid(tile):
        return tile in solids
    return isSolid

def makeGetNeighbors(jumps,levelStr,cant_mod,visited,isSolid,mod_allow,is_vertial):
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

        # Not sure what dng is, maybe mega man?
        # if GAME_IS == GAME_DNG:
        #     for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
        #         #nx, ny = (pos[0] + dx + maxX+1) % (maxX+1), (pos[1] + dy + maxY+1) % (maxY+1)
        #         nx, ny = pos[0] + dx, pos[1] + dy
        #         if nx < 1 or nx > maxX-1 or ny < 1 or ny > maxY-1:
        #             continue

        #         if not isSolid(levelStr[ny][nx]):
        #             neighbors.append([dist+1,(nx, ny, -1)])
    
        #         if isSolid(levelStr[ny][nx]):
        #             if mod_allow and (nx,ny) not in cant_mod:
        #                 mod_cost_dng = MOD_COST * random.randint(1, 10) ** 2
        #                 neighbors.append([dist+1+mod_cost_dng,(nx, ny, -1)])
        #     return neighbors
        
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

        if is_vertial:
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


def findPaths(solids,jumps,mod_allow,levelStr,params, is_vertical):
    maxX, maxY, startX, startY, goalX, goalY = params

    isSolid = makeIsSolid(solids)

    visited = set()
    cant_mod = set()

    # this prevents the level from being modded in such a way that moves the start or goal
    cant_mod.add((startX, startY))
    cant_mod.add((goalX, goalY))
    cant_mod.add((startX, startY+1))
    cant_mod.add((goalX, goalY+1))
    getNeighbors = makeGetNeighbors(jumps,levelStr,cant_mod,visited,isSolid,mod_allow,is_vertical)

    path = astar_shortest_path((startX,startY,-1), lambda pos: pos[0] == goalX and pos[1] == goalY, getNeighbors, lambda pos: 0)

    return path
