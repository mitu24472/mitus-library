import random
base = random.randint(2**31,2**32-1)
mod = 2**32-1
# mod = 2**61-1
hash_dic = {chr(i+97):i+1 for i in range(26)}
class rolling_hash():
    def __init__(self,S,base=None):
        self.string = S
        if base is None:
            self.baselist = baselist(base,len(S))
        else:
            self.baselist = base
        self.rolling_hash = rolling_hash_0_to_N(S)
    # S(l,r) のハッシュを計算します
    def slice(self,l,r):
        return self.rolling_hash[r] - self.rolling_hash[l] * self.baselist[r-l]
def rolling_hash_0_to_N(S):
    ans = [0,hash_dic[S[0]]]
    old_hash = hash_dic[S[0]]
    for i in range(1,len(S)):
        tmp = (old_hash*base+hash_dic[S[i]])%mod
        ans.append(tmp)
        old_hash = tmp
    return ans
def baselist(base,N):
    ans = [1,base]
    old = base
    for _ in range(N-1):
        ans.append(old*base)
        old *= base
        if old > mod:
            old %= mod
    return ans