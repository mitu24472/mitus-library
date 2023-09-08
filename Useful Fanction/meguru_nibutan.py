def meguru_nibutan(ok,ng,f):
    while abs(ok-ng) == 1:
        mid = (ok+ng)//2
        if f(mid):
            ok = mid
        else:
            ng = mid
    if f(ng):
        return ng
    else:
        return ok
