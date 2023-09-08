def is_inside(h,w):
    global H,W
    if (0 <= h < H) and (0 <= w < W):
        return True
    else:
        return False
def Grid_to_Graph(A,f,g):
    global H,W
    G = [[] for _ in range(H*W)]
    dxdy = [(0,1),(1,0),(-1,0),(0,-1)]
    for h,a in enumerate(A):
        for w,coa in enumerate(a):
            if f(coa):
                for d in dxdy:
                    if is_inside(h+d[0],w+d[1]):
                        if g(A[h+d[0]][w+d[1]]):
                            G[h*W+w].append((h+d[0])*W+w+d[1])
    return G