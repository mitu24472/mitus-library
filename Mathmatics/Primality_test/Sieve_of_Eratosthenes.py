#Eratosthenes 時間O(NloglogN) 空間O(N)
def Sieve_of_Eratosthenes(N):
    sieve = [True] * (N+1)
    sieve[0], sieve[1] = False, False
    for p in range(2, N+1):
        if not sieve[p]:
            continue
        q = p * 2
        while q <= N:
            sieve[q] = False
            q += p
    return sieve