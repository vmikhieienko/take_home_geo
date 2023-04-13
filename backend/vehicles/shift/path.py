# https://iq.opengenus.org/approximation-algorithm-for-travelling-salesman-problem/

import sys


def minimum_key(key: list[float], visited: list[int], n: int) -> int:
    min_val, min_index = sys.maxsize, 0
    for v in range(n):
        if not visited[v] and key[v] < min_val:
            min_val, min_index = key[v], v
    return min_index


# getting the Minimum Spanning Tree from the given graph
# using Prim's Algorithm
def prim_mst(graph: list[list[float]], n: int) -> list[list[int, int]]:
    parent = [-1] * n
    key = [sys.maxsize] * n
    visited = [False] * n

    # picking up the first vertex and assigning it to 0
    key[0] = 0

    # The Loop
    for count in range(n - 1):
        # checking and updating values wrt minimum key
        u = minimum_key(key, visited, n)
        visited[u] = True
        for v in range(n):
            if graph[u][v] and not visited[v] and graph[u][v] < key[v]:
                parent[v], key[v] = u, graph[u][v]

    return [[parent[i], i] for i in range(1, n)]


# getting the preorder walk of the MST using DFS
def dfs(edges: list[list[int]], n: int, start: int, visited_nodes: list[int], result: list[int]) -> None:
    # adding the node to final answer
    result.append(start)

    # checking the visited status
    visited_nodes[start] = True

    # using a recursive call
    for i in range(n):
        if i == start or not edges[start][i] or visited_nodes[i]:
            continue
        dfs(edges, n, i, visited_nodes, result)


def calculate_order(graph: list[list[float]]) -> list[int]:
    n = len(graph)
    v = prim_mst(graph, n)
    result = []

    # creating a dynamic matrix
    edges = [[0] * n for _ in range(n)]

    # setting up MST as adjacency matrix
    for i, j in v:
        edges[i][j] = 1
        edges[j][i] = 1

    # a checker function for the DFS
    visited = [False] * n

    # performing DFS
    dfs(edges, n, 0, visited, result)

    return result
