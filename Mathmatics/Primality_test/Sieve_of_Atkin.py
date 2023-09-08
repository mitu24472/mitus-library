#Atkin/Daniel J.Bernstainによる素数判定(2003) 時間O(N/log(log(N)) 空間O(N^(1/2+O(1)))) 10**7が限度っぽい 実質オーダーはO(Nlog(log(N)))ぐらいに感じる
import math
def Sieve_of_Atkin(lim):
    results = [2,3,5]
    sieve = [False] * (lim+1)
    factor = int(math.sqrt(lim))+1
    for i in range(1,factor):
        for j in range(1,factor):
            n = 4*i**2 + j**2
            if (n <= lim) and (n%12 == 1 or n%12 ==5):
                sieve[n] = not sieve[n]
            n = 3*i**2 + j**2
            if (n <= lim) and (n%12 == 7):
                sieve[n] = not sieve[n]
            if i>j:
                n = 3*i**2 - j**2
                if (n <= lim) and (n%12 == 11):
                    sieve[n] = not sieve[n]
    for index in range(5,factor):
        if sieve[index]:
            for jindex in range(index**2,lim,index**2):
                sieve[jindex] = False
    for index in range(7,lim):
        if sieve[index]:
            results.append(index)
    return results
print(len(Sieve_of_Atkin(50)))
