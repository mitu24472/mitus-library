import random
import cmath 
from itertools import zip_longest
def FFT(list_co,h,b,roun = True):
    butterfly_list = []
    n = len(list_co) 
    result = [0]*len(list_co)
    for i in range(n):
        reve_i = format(i,"b").zfill(h)
        butterfly_list.append(list_co[int(reve_i[::-1],2)])
    i = 1
    while i < n:
        for j in range(0,i):
            c += 1
            if not b:
                z = cmath.rect(1,-(2*cmath.pi*(-j))/(2*i)) 
            else:   
                z = cmath.rect(1,-(2*cmath.pi*j)/(2*i))
            for k in range(0,n,i*2):
                s = butterfly_list[j+k]
                t = butterfly_list[j+k+i] * z
                butterfly_list[j+k] = s + t
                butterfly_list[j+k+i] = s - t
        i = i*2
    if not b:
        for i in range(n):
            if roun:
                result[i] = round(butterfly_list[i].real / n)
            else:
                result[i] = (butterfly_list[i].real / n)
    else:
        result = butterfly_list
    print(c)
    return result
class FPS():
    def __init__(self,list_co):
        self.fps = list_co
        self.deg = len(list_co)
    def mul(self,other_polynomial):
        sum_deg = self.deg + other_polynomial.deg - 1
        i = 1
        while sum_deg > 2**i:
            i += 1
        n = 2**i
        self.fps = self.fps + [0] * (n - self.deg)
        copy_self_deg = self.deg
        self.deg = len(self.fps)
        other_polynomial.fps = other_polynomial.fps + [0] * (n - other_polynomial.deg)
        copy_other_deg = other_polynomial.deg
        other_polynomial.deg = len(other_polynomial.fps)
        self_FFT = FFT(self.fps,i,True)
        other_FFT = FFT(other_polynomial.fps,i,True)
        pro_FFT = []
        for a,b in zip(self_FFT,other_FFT):
            pro_FFT.append(a*b) 
        self.fps = self.fps[:copy_self_deg]
        self.deg = copy_self_deg
        other_polynomial.fps = other_polynomial.fps[:copy_other_deg]
        other_polynomial.deg = copy_other_deg
        return FPS(FFT(pro_FFT,i,False)[:copy_self_deg+copy_other_deg-1])
    
    def inversed(self,n):
        i = 1
        while 2**i < n:
            i += 1
        g = [0]
        g[0] = 1//self.fps[0]
        g = FPS(g)
        for _ in range(i):
            gn_f = self.mul(g)
            for k,j in enumerate(gn_f.fps):
                gn_f.fps[k] = -j
            gn_f.fps[0] += 2
            g = g.mul(gn_f)
            print(g.fps)
        g = FPS(g.fps[:n])
        return g
    
    def add(self,a,n):
        if n > self.deg:
            self.fps = self.fps + [0]*(n - self.deg - 1) + [a]
            self.deg = n
        else:
            self.fps[n] += a

    def added(self,a,n):
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

    def poly_added(self,other_polynomial):
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
    
    def poly_subed(self,other_polynomial):
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
    def divide(self,other_polinomial):
        if self.deg > other_polinomial.deg :
            print("計算できないよ！")
            return 0 
        f = FPS(list(reversed(self.fps.copy())))
        cf = f.inversed(other_polinomial.deg - self.deg)
        f = cf.mul(FPS([0]*(self.deg - other_polinomial.deg - 1) + [1]))
        g = FPS(list(reversed(other_polinomial.fps.copy())))
        result = f.mul(g)
        result = FPS(list(reversed(result.fps[:(other_polinomial.deg - self.deg)+1])))
        return result
FFT([random.randint(1,100) for _ in range(2**20)],20,True)