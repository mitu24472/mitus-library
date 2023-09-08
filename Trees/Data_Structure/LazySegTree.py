"""
使い方がかなりわかりにくい (抽象化遅延セグ木なので) 
S: class によって定義される self._d が持つ要素の型
F: class によって定義される self._lazy が持つ要素の型
op: 区間取得をしたいときにどのような演算をするか
e: 演算 op における単位元
comp(self._d,self._lazy): 配列 self._lazy を self._d に作用させるときにどのような演算をするか
mappng(親ノード, 子ノード): self._lazy に対して、それを子ノードに伝搬させる際にどのような演算を行うか
subsitution(操作が行われる区間 [l, r], x): self._lazy に [l, r] に x を作用させる際の self._lazy に加えられる値
id: 関数 mappng における恒等写像
n: 配列長
v: None だと全て 0 に、v が代入されているとその list をもとに LazySegTree を構築する
区間更新をしたいとき:https://betrue12.hateblo.jp/entry/2020/09/22/194541
"""
class LazySegTree:    
    def __init__(self, S, F, op, e, comp, mappng, subsitution, id, n, v=None):
        self._n = n
        self._op = op
        self._e = e
        self._comp = comp
        self._mapping = mappng
        self._subsitution = subsitution
        self._id = id
        self._log = (n - 1).bit_length()
        self._size = 1 << self._log
        self._d = [S(a=self._e())] * (2 * self._size)
        self._lazy = [F(a=self._id())] * (2 * self._size)
        if v is not None:
            for i in range(self._n):
                self._d[self._size + i] = v[i]
            for i in range(self._size - 1, 0, -1):
                self._update(i)

    #区間 [a, b] に x を作用させる
    def set(self, x, a, b, k=0,l=0,r=-1):
        if r == -1: r = self._n-1
        self.eval(k, l, r)
        if b <= l or r <= a:
            return
        if a <= l and r <= b:
            self._lazy[k] = self._mapping(self._lazy[k], self._subsitution(a, b, x))
            self.eval(k, l, r)
        else:
            self.set(x, a, b, k=2*k+1, l=l, r=(l+r)//2)
            self.set(x, a, b, k=2*k+2, l=(l+r)//2, r=r)
            self._d[k] = self._op(self._d[2*k+1], self._d[2*k+2])

    def eval(self, k, l, r):
        if self._lazy[k] != F(self._id()):
            self._d[k] = self._mapping(self._d[k], self._lazy[k])
            if r - l > 1:
                self._lazy[2*k+1] = self._comp(self._lazy[k],self._lazy[2*k+1])
                self._lazy[2*k+2] = self._comp(self._lazy[k],self._lazy[2*k+2])
            self._lazy[k] = F(self._id())
    def get(self, p):
        return self._d[p + self._size]

    def prod(self, a, b, k=0, l=0, r=-1):
        if r == -1: r = self._n
        if b <= l or r <= a: return S(0)
        self.eval(k, l, r)
        if a <= l and r <= b: return self._d[k]
        vl = self.prod(a, b, k=2 * k + 1, l=l, r=(l + r)//2)
        vr = self.prod(a, b, k=2 * k + 2, l=(l + r)//2, r=r)
        return S(vl.a+vr.a)
    
    def all_prod(self):
        return self._prod(0, self._n)

    def _update(self, k):
        self._d[k] = self._op(self._d[2 * k], self._d[2 * k + 1])
class S:
    def __init__(self, a):
        self.a = a
class F:
    def __init__(self, a):
        self.a = a
def op(x,y):
    a = S(x.a+y.a)
    return a
def e():
    return 0
def id():
    return 0
def subsitution(l, r, x):
    return S((r-l)*x)
def comp(x,y):
    a = F(x.a+y.a)
    return a
def mapping(x,y):
    a = S(a=(x.a)//2+y.a)
    return a
N, Q = map(int,input().split())
a = S(a=0)
print(a.a)
Lazy_Seg = LazySegTree(S, F, op, e, comp, mapping, subsitution, id, N)
for i in range(Q):
    q, s, *t = map(int,input().split())
    if q == 0:
        Lazy_Seg.set(t[1], s-1, t[0]-1)
    else:
        print(Lazy_Seg.prod(s-1, t[0]-1).a)