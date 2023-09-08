#関数実装
# s は始点 g は二次元リスト eは終点
#素の BFS は return していないので必要があれば適当なものを付け足してください
from collections import deque
def BFS(s,g):
    flag = [True] * len(g)
    flag[s] = False
    next = deque([s])
    while next:
        v = next.popleft()
        for j in g[v]:
            if not flag[j]:
                continue
            else:
                flag[j] = not flag[j]
                next.append(j)
#距離
def BFS_dist(s,g):
    flag = [True] * len(g)
    flag[s] = False
    next = deque([s])
    i = 0
    while next:
        i += 1
        now_next = next.copy
        next = deque([])
        while now_next:
            v = next.popleft()
            for j in g[v]:
                if not flag[j]:
                    continue
                else:
                    flag[j] = not flag[j]
                    next.append(j)
#経路復元
def BFS_path(s,e,g):
    flag = [True] * len(g)
    flag[s] = False
    next = deque([s])
    root = dict()
    while next:
        v = next.popleft()
        for j in g[v]:
            if not flag[j]:
                continue
            else:
                flag[j] = not flag[j]
                if not j in g[s]:
                    root[j] = v
                next.append(j)
        else:
            continue
        break
    now = e
    ans = [e]
    while now != s:
        ans.append(root[now])
        now = root[now]
    return ans
#ある点からの最長
def longest_BFS(s,g):
    flag = [True] * len(g)
    flag[s] = False
    next = deque([s])
    i = 0
    while next:
        all_next = next.copy()
        next = deque()
        while all_next:
            v = all_next.pop()
            for j in g[v]:
                if not flag[j]:
                    continue
                else:
                    flag[j] = not flag[j]
                    next.append(j)
        i += 1