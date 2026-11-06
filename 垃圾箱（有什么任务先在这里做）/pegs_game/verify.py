from itertools import combinations

def inv_of(st, n, k):
    s = set(st)
    w = "".join("U" if (i+1) in s else "R" for i in range(n))
    c = 0
    u = 0
    for ch in w:
        if ch == "U": u += 1
        else: c += u
    return c

def table(n, k):
    states = list(combinations(range(1, n+1), k))
    order = sorted(states, key=lambda st: inv_of(st, n, k), )
    win = {}
    for st in order:
        s = set(st); w = False
        for i, p in enumerate(st):
            for q in range(p+1, n+1):
                if q not in s:
                    ns = tuple(sorted(st[:i] + st[i+1:] + (q,)))
                    if not win[ns]:
                        w = True; break
            if w: break
        win[st] = w
    return win

print("independent backward-induction check (A = player to move wins = Alice wins)")
bad = []
for n in range(2, 14):
    row = []
    for k in range(1, n):
        win = table(n, k)
        a = win[tuple(range(1, k+1))]
        pred = not (n % 2 == 0 and k % 2 == 0)
        if a != pred: bad.append((n, k, a, pred))
        row.append(f"k={k}:{'A' if a else 'B'}")
    print(f"n={n:2d}  " + "  ".join(row))
print("MISMATCHES:", bad)
