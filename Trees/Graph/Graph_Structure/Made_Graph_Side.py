# N:頂点数 M:辺の数
def Made_Graph(N,M):
    Graph = [[] for _ in range(N)]
    for _ in range(M):
        x,y = miis()
        Graph[x].append(y)
        Graph[y].append(x)
    return Graph