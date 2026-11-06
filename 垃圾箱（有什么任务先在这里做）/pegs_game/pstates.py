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
        for i,p in enumerate(st):
            for q in range(p+1,n+1):
                if q not in s:
                    ns=tuple(sorted(st[:i]+st[i+1:]+(q,)))
                    if not win[ns]: w=True; break
            if w: break
        win[st]=w
    return win

def word(st,n):
    s=set(st); return "".join("U" if i in s else "R" for i in range(1,n+1))

for (n,k) in [(4,2),(5,2),(6,3),(6,2),(7,3),(7,2),(8,3),(8,4),(5,4),(6,4)]:
    win=table(n,k)
    P=[word(st,n) for st in combinations(range(1,n+1),k) if not win[st]]
    print(f"n={n},k={k}  init={word(tuple(range(1,k+1)),n)} ({'A' if win[tuple(range(1,k+1))] else 'B'})  #P={len(P)}")
    print("   P:", " ".join(sorted(P)))
    start=tuple(range(1,k+1)); s=set(start)
    good=[]
    for i,p in enumerate(start):
        for q in range(p+1,n+1):
            if q not in s:
                ns=tuple(sorted(start[:i]+start[i+1:]+(q,)))
                if not win[ns]: good.append((p,q,word(ns,n)))
    print("   winning first moves (peg at p -> hole q):", good)
