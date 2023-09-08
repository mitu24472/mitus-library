#作らないかも 閉路検出用に作ります
#関数実装
# s は始点 g は二次元リスト eは終点
#素の DFS は return していないので必要があれば適当なものを付け足してください
from collections import deque
def DFS(s,g):
    flag = [True] * len(g)
    flag[s] = False
    next = deque([s])
    while next:
        v = next.pop()
        for j in g[v]:
            if not flag[j]:
                continue
            else:
                flag[j] = not flag[j]
                next.append(j)