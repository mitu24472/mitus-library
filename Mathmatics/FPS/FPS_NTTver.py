#一変数用 FPS ライブラリ
from itertools import zip_longest
mod = 998244353
p = 23
a = 119
w = 3
Nthroots = [998244352, 911660635, 372528824, 929031873, 452798380, 922799308, 781712469, 476477967, 166035806, 258648936, 584193783, 63912897, 350007156, 666702199, 968855178, 629671588, 24514907, 996173970, 363395222, 565042129, 733596141, 267099868, 15311432]
inverse_Nthroots = [998244352, 86583718, 509520358, 337190230, 87557064, 609441965, 135236158, 304459705, 685443576, 381598368, 335559352, 129292727, 358024708, 814576206, 708402881, 283043518, 3707709, 121392023, 704923114, 950391366, 428961804, 382752275, 469870224]
v_list = [1, 499122177, 748683265, 873463809, 935854081, 967049217, 982646785, 990445569, 994344961, 996294657, 997269505, 997756929, 998000641, 998122497, 998183425, 998213889, 998229121, 998236737, 998240545, 998242449, 998243401, 998243877, 998244115, 998244234]
"""
w_a = pow(w,a,mod)
for _ in range(p):
    Nthroots.append(w_a)
    inverse_Nthroots.append(pow(w_a,mod-2,mod))
    w_a = pow(w_a,2,mod)
Nthroots.reverse()
inverse_Nthroots.reverse()
print(Nthroots)
print(inverse_Nthroots)
"""
def bit_reverse(n):
    n = (n >> 16) | (n << 16)
    n = ((n & 0xff00ff00) >> 8) | ((n & 0x00ff00ff) << 8)
    n = ((n & 0xf0f0f0f0) >> 4) | ((n & 0x0f0f0f0f) << 4)
    n = ((n & 0xcccccccc) >> 2) | ((n & 0x33333333) << 2)
    n = ((n & 0xaaaaaaaa) >> 1) | ((n & 0x55555555) << 1)
    return n  
reverse_list = [bit_reverse(i) for i in range(2**23)]
def FFT(list_co,h,b):
    global Nthroots, inverse_Nthroots
    butterfly_list = []
    n = len(list_co) 
    result = [0]*len(list_co)
    if h == 0:
        return list_co
    for i in range(n):
        butterfly_list.append(list_co[reverse_list[i] >> (32 - h)])
    i = 1
    l = 0
    while i < n:
        for j in range(0,i):
            if not b:
                z = pow(inverse_Nthroots[l],j,mod)
            else:   
                z = pow(Nthroots[l],j,mod)
            for k in range(0,n,i*2):
                butterfly_list[j+k],butterfly_list[j+k+i] = (butterfly_list[j+k]+butterfly_list[j+k+i]*z)%mod, (butterfly_list[j+k]-butterfly_list[j+k+i]*z)%mod
        i = i*2
        l += 1
    if not b:
        for i in range(n):
            result[i] = butterfly_list[i] * v_list[h]  % mod
    else:
        return butterfly_list
    return result
 
class FPS():
    def __init__(self,list_co):
        self.fps = list_co
        self.deg = len(list_co)
    def __mul__(self,other_polynomial):
        sum_deg = self.deg + other_polynomial.deg - 1
        i = 1
        while sum_deg > 2**i:
            i += 1
        n = 2**i
        self_FFT = FFT(self.fps+[0] * (n - self.deg),i,True)
        other_FFT = FFT(other_polynomial.fps+[0] * (n - other_polynomial.deg),i,True)
        pro_FFT = []
        for a,b in zip(self_FFT,other_FFT):
            pro_FFT.append(a*b%mod)
        return FPS(FFT(pro_FFT,i,False)[:self.deg+other_polynomial.deg-1])

    def mul(self,g):
        ans = [0] * (g.deg*self.deg-1)
        for i in range(g.deg):
            if g.fps[i] == 0:
                continue
            for j in range(self.deg):
                ans[i+j] += g.fps[i]*self.fps[j]
    def inversed(self,n):
        i = 1
        while 2**i < n:
            i += 1
        g = [0]
        g[0] = pow(self.fps[0],mod-2,mod)
        g = FPS(g)
        for _ in range(i):
            gn_f = self * g
            for k,j in enumerate(gn_f.fps):
                gn_f.fps[k] = mod-j
            gn_f.fps[0] += 2
            g = g * gn_f
        g = FPS(g.fps[:n])
        return g
    
    def add(self,a,n):
        if n > self.deg:
            self.fps = self.fps + [0]*(n - self.deg - 1) + [a]
            self.deg = n
        else:
            self.fps[n] += a
 
    def add(self,a,n):
        f = FPS(self.fps.copy())
        if n > f.deg:
            f.fps = f.fps + [0]*(n - f.deg - 1) + [a]
            f.deg = n
        else:
            f.fps[n] += a
        return f
    
    def poly_add(self,other_polynomial):
        self.deg = max(self.deg,other_polynomial.deg)
        self.fps = self.fps + [0]*(self.deg - len(self.fps))
        i = 0
        for s,o in zip_longest(self.fps,other_polynomial.fps):
            if o == None:
                o = 0
            if s == None:
                s = 0
            self.fps[i] = s+o
            i += 1
 
    def poly_sub(self,other_polynomial):
        self.deg = max(self.deg,other_polynomial.deg)
        self.fps = self.fps + [0]*(self.deg - len(self.fps))
        i = 0
        for s,o in zip_longest(self.fps,other_polynomial.fps):
            if o == None:
                o = 0
            if s == None:
                s = 0
            self.fps[i] = s-o
            i += 1
 
    def __add__(self,other_polynomial):
        f = FPS(self.fps.copy())
        f.deg = max(f.deg,other_polynomial.deg)
        f.fps = f.fps + [0]*(f.deg - len(f.fps))
        i = 0
        for s,o in zip_longest(f.fps,other_polynomial.fps):
            if o == None:
                o = 0
            if s == None:
                s = 0
            f.fps[i] = s+o
            i += 1
        return f
    
    def __sub__(self,other_polynomial):
        f = FPS(self.fps.copy())
        f.deg = max(f.deg,other_polynomial.deg)
        f.fps = f.fps + [0]*(f.deg - len(f.fps))
        i = 0
        for s,o in zip_longest(f.fps,other_polynomial.fps):
            if o == None:
                o = 0
            if s == None:
                s = 0
            f.fps[i] = s-o
            i += 1
        return f
    
    def differ(self,n):
        g = [(n+1)*i for n,i in enumerate(self.fps[1:n+1])]
        return FPS(g)
    
    def integral(self,n):
        g = [0] + [i / (n+1) for n,i in enumerate(self.fps[:n+1])]
        return FPS(g)
    
    def log(self,n):
        if self.fps[0] != 1:
            print("計算できないよ！")
            return 0
        dif_div_fx = self.differ(n).mul(self.inversed(n))
        return dif_div_fx.integral(n)
    
    def exp(self,n):
        if self.fps[0] != 0:
            print("計算できないよ！")
            return 0
        g = [0]
        g[0] = 1
        g = FPS(g)
        co = FPS([1])
        f_k = FPS(self.fps.copy())
        print(g.fps)
        for k in range(1,n):
            co = co.mul(FPS([1/k]))
            print(co.fps)
            g.poly_add(f_k.mul(co))
            f_k = f_k.mul(self)
            print(f_k.fps)
        return g
    def __truediv__(self,other_polinomial):
        if self.deg > other_polinomial.deg :
            print("計算できないよ！")
            return 0 
        f = FPS(list(reversed(self.fps.copy())))
        cf = f.inversed(other_polinomial.deg)
        f = cf * FPS([0]*(self.deg - other_polinomial.deg - 1) + [1])
        g = FPS(list(reversed(other_polinomial.fps.copy())))
        result = f * g
        result = FPS(list(reversed(result.fps[:(other_polinomial.deg - self.deg)+1])))
        return result
N,M = map(int,input().split())
f = FPS(list(map(int,input().split())))
g = FPS(list(map(int,input().split())))
result = (f / g).fps
for i,r in enumerate(result):
    if r > 1000:
        result[i] = r - mod
print(*result)