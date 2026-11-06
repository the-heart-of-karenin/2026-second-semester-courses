import sys
from functools import lru_cache
from itertools import combinations
sys.setrecursionlimit(100000)

def grundy(n):
    @lru_cache(maxsize=None)
    def g(state):
        s=set(state); vals=set()
        for i,p in enumerate(state):
            for q in range(p+1,n+1):
                if q not in s:
                    vals.add(g(tuple(sorted(state[:i]+state[i+1:]+(q,)))))
        m=0
        while m in vals: m+=1
        return m
    return g

def gval(n,k,state=None):
    g=grundy(n)
    if state is None: state=tuple(range(1,k+1))
    return g(tuple(state))

# --- claim: packed(n,k) is P iff n,k both even
bad=[]
for n in range(2,15):
    g=grundy(n)
    for k in range(1,n):
        v=g(tuple(range(1,k+1)))
        if (v==0) != (n%2==0 and k%2==0): bad.append((n,k,v))
print("A) packed(n,k): P iff n,k even  -> mismatches:",bad)

# --- claimed target positions after Alice's first move (must be P, and isomorphic to a packed subgame)
bad2=[]; badiso=[]
for n in range(2,15):
    g=grundy(n)
    for k in range(1,n):
        if n%2==0 and k%2==0: continue          # Bob wins; no Alice move
        if n%2==0 and k%2==1:
            target=tuple(sorted(set(range(2,k+1))|{n}))       # peg1 -> hole n
            sub=(n-2,k-1)                                      # board holes 2..n-1
        elif n%2==1 and k%2==0:
            target=tuple(range(2,k+2))                         # peg1 -> hole k+1
            sub=(n-1,k)                                        # board holes 2..n
        else:
            target=tuple(sorted(set(range(1,k))|{n}))          # peg k -> hole n
            sub=(n-1,k-1)                                      # board holes 1..n-1
        v=g(target)
        if v!=0: bad2.append((n,k,target,v))
        # is the target reachable by a legal first move from packed(1..k)?
        start=set(range(1,k+1))
        ok=any(y>x and y not in start and tuple(sorted((start-{x})|{y}))==target
               for x in start for y in range(1,n+1))
        if not ok: bad2.append(("ILLEGAL-FIRST-MOVE",n,k,target))
        # Grundy isomorphism with the packed subgame on a translated even board
        m,kk=sub
        # translate target into board 1..m  (board = the m consecutive holes mentioned above)
        if n%2==0 and k%2==1: board=list(range(2,n)); pegs=[p-1 for p in target if p<n]
        elif n%2==1 and k%2==0: board=list(range(2,n+1)); pegs=[p-1 for p in target]
        else: board=list(range(1,n)); pegs=[p for p in target if p<n]
        assert len(board)==m and (m==0 or board==list(range(board[0],board[0]+m))), (n,k,board)
        assert sorted(pegs)==list(range(1,kk+1)), (n,k,target,pegs)
        vsub=grundy(m)(tuple(range(1,kk+1)))
        if vsub!=v: badiso.append((n,k,v,vsub))
print("B) Alice's prescribed first move is legal and lands on a P-position -> problems:",bad2)
print("C) Grundy value of that position == Grundy value of packed subgame (isomorphism) -> problems:",badiso)
