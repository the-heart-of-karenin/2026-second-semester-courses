import sys
from functools import lru_cache
from itertools import combinations

sys.setrecursionlimit(100000)

def make_g(n):
    @lru_cache(maxsize=None)
    def g(state):
        s = set(state)
        vals = set()
        for i, p in enumerate(state):
            for q in range(p + 1, n + 1):
                if q not in s:
                    ns = tuple(sorted(state[:i] + state[i + 1:] + (q,)))
                    vals.add(g(ns))
        m = 0
        while m in vals:
            m += 1
        return m
    return g

rows = []
for n in range(2, 11):
    g = make_g(n)
    line = []
    for k in range(1, n):
        start = tuple(range(1, k + 1))
        val = g(start)
        line.append(f"k={k}:{'A' if val else 'B'}({val})")
    rows.append(f"n={n:2d}  " + "  ".join(line))
print("\n".join(rows))
