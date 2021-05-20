from collections import deque

def generate_link_bfs(grammar, start, end, additional_columns):
    '''
    Based off of: https://www.redblobgames.com/pathfinding/a-star/introduction.html
    '''
    # generate path of minimum length with an n-ram
    start_link = grammar.generate(start, additional_columns)
    min_path = start + start_link

    # BFS to find the ending prior
    path_found = False
    queue = deque()
    came_from = {}

    start_prior = ','.join(min_path[-(grammar.n - 1):])
    start_prior = f'{start_prior},0'
    end_prior = ','.join(end[:grammar.n - 1])

    queue.append(start_prior)

    while queue:
        prior = queue.popleft()
        split_prior = prior.split(',')
        path_length = int(split_prior.pop()) + 1

        output = grammar.get_unweighted_output(','.join(split_prior))
        if output != None:
            for new_column in output:
                new_prior_queue = deque(split_prior, maxlen=grammar.n - 1)
                new_prior_queue.append(new_column)
                new_prior = ','.join(list(new_prior_queue))
                new_prior_with_length = f'{new_prior},{path_length}' 

                if new_prior_with_length not in came_from:
                    queue.append(new_prior_with_length)
                    if new_prior == end_prior and path_length >= grammar.n:
                        end_prior = f'{end_prior},{path_length}'
                        came_from[new_prior_with_length] = prior
                        path_found = True
                        break
                    else:
                        came_from[new_prior_with_length] = prior
            
            if path_found:
                break
    
    if not path_found:
        return None

    # reconstruct path
    path = []
    current = end_prior

    while current != start_prior:
        split_current = current.split(',')
        split_current.pop()
        path.insert(0, split_current[-1])

        current = came_from[current]

    return start_link + path[:-(grammar.n - 1)]
    
    # this is dead code but may be useful for debugging in the future
    # if not grammar.sequence_is_possible(start + link + end):
    #     from Utility.GridTools import columns_into_rows

    #     print()
    #     print(grammar.sequence_is_possible(start))
    #     print(grammar.sequence_is_possible(link))
    #     print(grammar.sequence_is_possible(end))
    #     print('start + link:', grammar.sequence_is_possible(start + link))
    #     print('link + end:', grammar.sequence_is_possible(link + end))
    #     link.insert(0, '==============')
    #     link.append('==============')
    #     print()
    #     print('\n'.join(columns_into_rows(start + link + end)))
    #     import sys
    #     sys.exit(-1)
    

def generate_link_mcts(grammar, start, end, additional_columns, include_path_length=False):
    '''
    Based off of work from Summerville, MCMCTS 4 SMB.
    '''
    raise NotImplementedError()

    # generate path of minimum length with an n-ram
    min_path = start + grammar.generate(start, additional_columns)

    # BFS to find the ending prior
    path_found = False
    queue = deque()
    came_from = {}

    start_prior = ','.join(min_path[-(grammar.n - 1):])
    start_prior = f'{start_prior},0'
    end_prior = ','.join(end[:grammar.n - 1])

    queue.append(start_prior)

    while queue:
        prior = queue.popleft()
        split_prior = prior.split(',')
        path_length = int(split_prior.pop()) + 1

        output = grammar.get_unweighted_output(','.join(split_prior))
        if output != None:
            for new_column in output:
                new_prior_queue = deque(split_prior, maxlen=grammar.n - 1)
                new_prior_queue.append(new_column)
                new_prior = ','.join(list(new_prior_queue))
                new_prior_with_length = f'{new_prior},{path_length}' 

                if new_prior_with_length not in came_from:
                    queue.append(new_prior_with_length)
                    if new_prior == end_prior and path_length >= grammar.n:
                        end_prior = f'{end_prior},{path_length}'
                        came_from[new_prior_with_length] = prior
                        path_found = True
                        break
                    else:
                        came_from[new_prior_with_length] = prior
            
            if path_found:
                break
    
    if not path_found:
        if include_path_length:
            return None, -1
        return None

    # reconstruct path
    path = []
    current = end_prior

    while current != start_prior:
        split_current = current.split(',')
        split_current.pop()
        path.insert(0, split_current[-1])

        current = came_from[current]

    full_map = min_path + path + end[grammar.n - 1:]
    if include_path_length:
        return full_map, len(full_map) - len(start) - len(end)
    
    return full_map