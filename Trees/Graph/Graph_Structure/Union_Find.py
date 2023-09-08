#クラス実装
#座標圧縮によって(α(n))
class UnionFind():

    def __init__(self, n):
        self.par = [-1] * n
        self.rank = [0] * n
        self.siz = [1] * n

    def root(self, x):
        if self.par[x] == -1: return x 
        else:
          self.par[x] = self.root(self.par[x]) 
          return self.par[x]


    def issame(self, x, y):
        return self.root(x) == self.root(y)


    def unite(self, x, y):
        rx = self.root(x)
        ry = self.root(y)
        if rx == ry: return False
        if self.rank[rx] < self.rank[ry]:
            rx, ry = ry, rx
        self.par[ry] = rx 
        if self.rank[rx] == self.rank[ry]: 
            self.rank[rx] += 1
        self.siz[rx] += self.siz[ry]
        return True
    def size(self, x):
        return self.siz[self.root(x)]