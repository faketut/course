= Problem 1 - Persistent Vertices
Let $G=(V,E)$ be a finite directed graph (without self-loops). Call a vertex $v$ \textit{persistent} if there exists an infinite directed walk starting at $v$. Vertices and edges may be repeated in a walk.\
(a). Characterize persistent vertices in terms of directed cycles.\
Persistent vertices are those can reach a directed cycle.\
(b) Design an $O(n+m)$-time algorithm that finds all persistent vertices.\
Algo:\
```
def find_persistent_vertices_kosaraju(G):
    finishing_order = get_dfs_finishing_order(G)
    
    G_r = reverse_graph(G)
    
    sccs = []
    visited = set()
    for v in reversed(finishing_order):
        if v not in visited:
            comp = []
            dfs_on_reversed(G_r, v, visited, comp)
            sccs.append(comp)
            
    persistent = {v: False for v in G.V}
    valid_scc_nodes = []
    
    for comp in sccs:
        if len(comp) > 1:
            for v in comp:
                valid_scc_nodes.append(v)
                persistent[v] = True

    queue = list(valid_scc_nodes)
    reachable_visited = set(valid_scc_nodes)
    
    while queue:
        curr = queue.pop(0)
        persistent[curr] = True
        for neighbor in G_r.neighbors(curr):
            if neighbor not in reachable_visited:
                reachable_visited.add(neighbor)
                queue.append(neighbor)
                
    return persistent
```
Correctness: \
The lecture justifys the kosaraju algo's correctness of finding all SCCs. SCCs with size > 1 has directed cycles because they have no self-loops. The BFS on the reversed graph marks the nodes can be reached from the persistent SCCs, which means they can reach a directed cycle in the original graph. Therefore, all persistent vertices are correctly identified.\
Time Complexity:\
The Kosaraju algorithm runs in O(n + m) time, where n is the number of vertices and m is the number of edges. The BFS on the reversed graph also runs in O(n + m) time. Therefore, the overall time complexity of the algorithm is O(n + m).\
(c) A student claims that a vertex is persistent if and only if its out-degree is positive. Give a counterexample and explain the error.
