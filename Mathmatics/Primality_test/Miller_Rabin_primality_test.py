#Gary L.Miller/Michael Rabin(1975) 
#十分小さいN(<3*10**14)について O((logn)**3) 繰り返し二乗法によって O((logn)**2)
#pythonのpowは勝手に繰り返し二乗法を使ってくれる
def Miller_Rabin(N):
    if N <= 1:
        return False
    k = 0
    m = N - 1
    while m & 1 == 0:
        k += 1
        m >>= 1
    assert(2**k*m == N-1)
    task = [2,3,5,7,11,13,17]
    def test(N,t):
        b = pow(t,m,N)
        if b == 1:
            return True
        for i in range(0,k):
            if b == N - 1:
                return True
            b = pow(b,2,N)
        return False
    for t in task:
        if t >= N:
            break
        if not test(N,t):
            return False
    return True