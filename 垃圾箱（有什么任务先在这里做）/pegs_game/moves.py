from itertools import combinations

def inv_of(st, n):
    s=set(st); u=0; c=0
    for i in range(1,n+1):
        if i in s: u+=1
        else: c+=u
    return c

def table(n,k):
    states=list(combinations(range(1,n+1),k))
    order=sorted(states,key=lambda st: inv_of(st,n))
    win={}
    for st in order:
        s=set(st); w=False
        for t,p in enumerate(st):
            for q in range(p+1,n+1):
                if q not in s:
                    ns=tuple(sorted(st[:t]+st[t+1:]+(q,)))
                    if not win[ns]: w=True; break
            if w: break
        win[st]=w
    return win

def word(st,n):
    s=set(st); return "".join("U" if i in s else "R" for i in range(1,n+1))

for n in range(3,13):
    for k in range(1,n):
        if n%2==0 and k%2==0: continue
        win=table(n,k); start=tuple(range(1,k+1)); s=set(start)
        gm=[]
        for t,p in enumerate(start):
            for q in range(p+1,n+1):
                if q not in s:
                    ns=tuple(sorted(start[:t]+start[t+1:]+(q,)))
                    if not win[ns]: gm.append((p,q,word(ns,n)))
        print(f"n={n:2d} k={k:2d} (N={n-k:2d}) init={'A' if win[start] else 'B'}  winners: {gm}")
