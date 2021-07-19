from Utility.GridTools import columns_into_grid_string
from collections import deque
from math import sqrt, log, exp
from random import random, choice, randint
from itertools import repeat


##################################### BFS #####################################
# - exhaustive search, use a flag and life is good
# - if path has better characteristics, run agent else continue
# - change to stamina branch of DG, how many iterations to run for DG. Add third dimension if possible.
# - what % of the links asked to make work versus do not
# - % that the segments could be completed
# - what happens if a walkthrough fails? PIck x segments, if linking fails then
#   pick new segments. Report on how many times a link failed to find a level.
# - Seth makes overleaf
# - write the paper
def generate_link_bfs(grammar, start, end, additional_columns, agent=None, max_length=30):
    '''
    Based off of: https://www.redblobgames.com/pathfinding/a-star/introduction.html
    '''
    print('WARNING :: I do not handle two priors being exactly the same yet.')
    print('TODO :: Rename generate_link_bfs to generate_link')
    assert grammar.sequence_is_possible(start)
    assert grammar.sequence_is_possible(end)

    # print()
    # print(start)
    # print(end)
    # print()

    if agent != None:
        assert agent(start) == 1.0
        assert agent(end) == 1.0

    if additional_columns == 0 and grammar.sequence_is_possible(start + end):
        return []

    # generate path of minimum length with an n-gram
    start_link = grammar.generate(tuple(start), additional_columns)
    min_path = start + start_link

    # BFS to find the ending prior
    queue = deque()
    came_from = {}

    start_node = (tuple(min_path[-(grammar.n - 1):]), 0)
    end_prior = tuple(end[:grammar.n - 1])
    iterations = 500
    queue.append(start_node)
    path = None

    # loop through queue until a path is found
    while queue:
        node = queue.popleft()
        if node[1] + 1 > 30:
                continue
            
        current_prior = node[0]
        output = grammar.get_unweighted_output_list(current_prior)
        if output == None:
            continue
        # print(len(queue), len(current_path), len(output))
        # print(current_path, prior, output)

        for new_column in output:
            # build the new prior with the slice found by removing the first 
            # slice
            new_prior = current_prior[1:] + (new_column,)
            new_node = (new_prior, node[1] + 1)

            if new_node in came_from:
                continue

            # if the prior is not the end prior, add it to the search queue and
            # continue the search
            came_from[new_node] = node
            queue.append(new_node)
            if new_prior != end_prior:
                continue

            # reconstruct path
            path = []
            temp_node = new_node
            while temp_node != start_node:
                path.insert(0, temp_node[0][-1])
                temp_node = came_from[temp_node]

            # only use the path if we have constructed a path that is larger 
            # than n.
            if len(path) >= grammar.n:
                # TODO: this link creation is wrong right now but not the bigger issue for right now :/
                # link = start_link + new_path[:-(grammar.n - 1)]
                link =  path[:-(grammar.n - 1)]
                if agent != None:
                    playability = agent(start + link + end)
                    if playability == 1.0:
                        return link
                    else:
                        iterations -=1

                        if iterations <= 0:
                            print()
                            print(columns_into_grid_string(start))
                            print()
                            print(columns_into_grid_string(end))
                            print()
                            print('here!!!!!!!!')
                            import sys
                            sys.exit(-1)
                else:
                    return link
            
    # No link found
    print('ERROR :: no link found!')
    return None
