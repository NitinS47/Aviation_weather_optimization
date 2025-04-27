import heapq

def dijkstra(graph, start, end):
    queue = [(0, start)]
    visited = {}
    while queue:
        (cost, node) = heapq.heappop(queue)
        if node == end:
            return cost
        if node in visited:
            continue
        visited[node] = cost
        for neighbor, weight in graph[node].items():
            heapq.heappush(queue, (cost + weight, neighbor))
    return float('inf')