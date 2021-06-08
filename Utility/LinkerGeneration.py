from collections import deque
from math import sqrt, log, exp

##################################### BFS #####################################
def generate_link_bfs(grammar, start, end, additional_columns):
    '''
    Based off of: https://www.redblobgames.com/pathfinding/a-star/introduction.html

    @TODO: This should really not rely so heavily on splits and all that nonsense.
    The datastructures can definitely be simplified and improved. 
    '''
    if additional_columns == 0 and grammar.sequence_is_possible(start + end):
        return []

    # generate path of minimum length with an n-ram
    start_link = grammar.generate(start, additional_columns)
    min_path = start + start_link

    # BFS to find the ending prior
    queue = deque()
    came_from = {}

    start_node = (tuple(min_path[-(grammar.n - 1):]), 0)
    end_prior = tuple(end[:grammar.n - 1])
    end_node = None

    queue.append(start_node)

    while queue:
        node = queue.popleft()
        prior = node[0]
        path_length = node[1]

        output = grammar.get_unweighted_output(prior)
        if output != None:
            for new_column in output:
                new_node = (tuple(prior[1:]) + (new_column,), path_length + 1)

                if new_node not in came_from:
                    if new_node[0] == end_prior and path_length >= grammar.n:
                        end_node = new_node
                        came_from[end_node] = node
                        break
                    else:
                        came_from[new_node] = node
                        queue.append(new_node)
            
            if end_node != None:
                break
    
    if end_node == None:
        return None

    # reconstruct path
    path = []

    while end_node != start_node:
        path.insert(0, end_node[0][-1])
        end_node = came_from[end_node]

    return start_link + path[:-(grammar.n - 1)]

##################################### MCTS #####################################
# A node has it's sum score (w), the number of times it has been seen (n),
# whether the end prior can be found by this node (s), and its associated 
# prior (p), and relevant children (B for baby since C is taken).
#
#   [w, n, s, p, []]
#
# We end the rollout stage either once a max_path_size is reached or,
# preferably, the end prior is found. 
W = 0
N = 1
S = 2
P = 3
B = 4

# We follow convention of MCTS with C = sqrt(2). This can be used to explore the
# tradeoff between exploration and exploitation.
C = sqrt(2)

def best_child_node(node, t, end_prior, require_seen=False):
    best_index = -1
    best_uct = -1
    for i, child in enumerate(node[B]):
        if require_seen and not child[S]:
            continue 

        if not require_seen and child[S] == end_prior:
            continue
        
        # uct = (w/n) + C*sqrt(log(t)/n)
        uct = (child[W]/child[N]) + C*sqrt(log(t)/child[N])
        if uct > best_uct:
            best_index = i
            best_uct = uct

    return best_index

def generate_link_mcts(
    grammar, 
    start, 
    end, 
    feature_dimensions, 
    feature_targets,
    after_found_simulations=5_000,
    max_simulations=10_000,
    max_path_size=30):
    '''
    Based off of work from Summerville, MCMCTS 4 SMB.

    The problem with this approach is that some grammars have a large space
    to get from the start prior to the end prior. MCTS can take a lot of
    iterations to find a link. Because this is offline, we can do it a bit
    intelligently. In real time, this is not an option. But here we'll go
    till a connection is found and then do 50,000 more iterations. We'll also
    have a max number of simulations just in case. The code that calls this
    function, therefore, should be prepared to receive a value of None and
    use the BFS alternative. 
    '''
    # We only want to create a link if we have to.
    if grammar.sequence_is_possible(start + end):
        return []   

    # initialization
    root = [0, 0, False, tuple(start[-(grammar.n - 1):]), []]
    end_prior = tuple(end[:grammar.n - 1])
    t = 1

    # t represents the total number of simulations and is used in the upper
    # confidence bound applied to tress (UCT).
    for t in range(1, max_simulations):
        if root[S]:
            if after_found_simulations <= 0:
                break
            else:
                after_found_simulations -= 1

        # roll out to leaf and make sure that the leaf in question is not at
        # the end prior since that is already complete. During the rollout 
        # stage the level is built for calculating the score. We also keep a
        # history of the path taken to pass the score to the used nodes. 
        history = []
        level = list(root[P])
        node = root
        path_size = 0

        while len(node[B]) != 0:
            best_index = best_child_node(node, t, end_prior)
            
            history.append(best_index)
            node = node[B][best_index]
            level.append(node[P][-1])
            path_size += 1

            if path_size > max_path_size:
                break

        # At leaf, build a new child node. The score is the sum of squares difference
        # of the target values for the feature dimensions and what is actually found.
        # The sigmoid of the result is used to guarantee a value between 0 and 1.
        p = node[P]
        output_new_tokens = grammar.get_unweighted_output(p)

        for new_token in output_new_tokens:
            new_p = p[1:] + (new_token,)
            
            # check if the targer prior was found. If not and this is the index
            # where we want to roll out more, we do so without keeping track of
            # history. We do, though, keep track of the level to get a score.
            seen = new_p == end_prior
            if not seen:
                level.append(new_token)
                prior = new_p
                while len(level) < max_path_size and not seen:
                    next_token = grammar.get_output(prior)
                    level.append(next_token)
                    prior = prior[1:] + (next_token,)
                    # seen = new_p == end_prior

            seen &= path_size >= grammar.n # link cannot be empty

            root[S] |= seen
            score = sum([(feature_targets[i] - feature_dimensions[i](level))**2 for i in range(len(feature_dimensions))])
            score = 1/(1 + exp(-score))
            node[B].append([score, 1, seen, new_p, []])

            node = root
            for index in history:
                node[W] += score
                node[N] += 1
                node[S] |= seen
                node = node[B][index]
            node[W] += score
            node[N] += 1
            node[S] |= seen

    if root[S]:
        link = []
        while root[P] != end_prior:
            best_index = best_child_node(root, t, end_prior, require_seen=True)
            root = root[B][best_index]
            link.append(root[P][-1])

        return link[:-(grammar.n - 1)]

    return None