"""Physical-edge audit definitions; directed families use ALL proper subsets."""
from pathlib import Path
import json, functools, itertools
ROOT = Path(__file__).resolve().parent.parent
OUT = Path(__file__).resolve().parent
PAIRS = list(itertools.combinations(range(7), 2))

class Graph:
    def __init__(self, edges, n=7):
        self.edges = tuple(map(tuple, edges)); self.n = n
        self.full = (1 << n)-1; self.M = len(edges)
        self.cuts = {}
        for x in range(1, self.full):
            a=b=0
            for e,(u,v) in enumerate(self.edges):
                if x>>u&1 and not x>>v&1: a |= 1<<e
                if x>>v&1 and not x>>u&1: b |= 1<<e
            self.cuts[x]=(a,b,(a|b).bit_count())
        self.lam = min(c[2] for c in self.cuts.values())
    def out(self,s,x):
        a,b,_=self.cuts[x]; return ((~s&a)|(s&b)).bit_count()
    @functools.lru_cache(maxsize=100000)
    def legal(self,s):
        return 0<=s<1<<self.M and all(self.out(s,x)>=2 for x in self.cuts)
    def arc(self,s,e):
        u,v=self.edges[e]; return (v,u) if s>>e&1 else (u,v)
    def family(self,s,e,outdegree):
        u,v=self.arc(s,e)
        return [x for x in self.cuts if x>>u&1 and not x>>v&1 and self.out(s,x)==outdegree]
    def minimal(self,s,e):
        b=self.family(s,e,2)
        if not b: raise AssertionError('INTERNAL_INCONSISTENCY: missing tight blocker')
        a=self.full
        for x in b: a &= x
        u,v=self.arc(s,e)
        assert a>>u&1 and not a>>v&1 and self.out(s,a)==2, 'minimal blocker validation failed'
        return a,b
    def skeleton(self):
        shores=[x for x,c in self.cuts.items() if not x&1 and c[2]==5]
        for x,y in itertools.combinations(shores,2):
            if x&y and x&y!=x and x&y!=y:
                raise AssertionError(f'ODD_MINCUT_LAMINARITY_FAILURE: {x},{y}')
        parent={x:min([y for y in shores+[self.full] if x!=y and x&y==x], key=int.bit_count) for x in shores}
        return shores,parent
    def phases(self,s):
        shores,_=self.skeleton(); result=[]
        for x in shores:
            o=self.out(s,x); assert o in (2,3)
            result.append('OUT_SURPLUS' if o==3 else 'IN_SURPLUS')
        return result
    def verify_flip(self,s,t,e):
        assert s^t==1<<e and self.legal(s) and self.legal(t)
        shores,_=self.skeleton(); u,v=self.arc(s,e); crossed=[]
        for x in shores:
            before=self.out(s,x);after=self.out(t,x)
            assert before in (2,3) and after in (2,3)
            if bool(x>>u&1)!=bool(x>>v&1):
                assert before==(3 if x>>u&1 else 2)
                assert before+after==5;crossed.append(x)
            else: assert before==after
        return crossed

def saved_pairs():
    cases=[]; seen=set()
    def add(d,dataset,origin,paths):
        edges=d.get('physical_edges') or [uv for uv,m in zip(PAIRS,d['m']) for _ in range(m)]
        key=(tuple(map(tuple,edges)),d['source'],d['target'])
        if key in seen:return
        seen.add(key)
        cases.append(dict(dataset=dataset,origin=str(origin),graph_class=d.get('graph_class_index'),
                          source=d['source'],target=d['target'],physical_edges=edges,paths=paths,
                          coverage='SAVED_WITNESSES_ONLY',distance=d.get('distance')))
    for m in (18,19,20):
        p=ROOT/f'm{m}_results/records.jsonl'
        for line in p.read_text().splitlines():
            d=json.loads(line)
            if d['distance'] != (5 if m==18 else 7):continue
            add(d,f'M{m}_saved_hard',p,[dict(kind='shortest_progress_path',nodes=d['path'],reported_distance=d['distance'])])
    old=Path('C:/Users/HUAWEI/Desktop/CodexWorkspace/STEP1_CORRECTNESS_work/n7_hard_obstruction')
    candidates=sorted((old/'smoke_record/candidates').glob('*.json'))
    candidates+=sorted(Path('D:/GraphOrientationSearch_n7_M18/candidates').glob('*.json'))
    for p in candidates:
        d=json.loads(p.read_text()); paths=[]
        for field,kind in [('first_correction_path','shortest_first_correction_path'),('first_below_initial_path','shortest_progress_path'),('target_path','shortest_source_target_path')]:
            if d.get(field):paths.append(dict(kind=kind,nodes=d[field],reported_distance=len(d[field])-1))
        add(d,'M18_old_explicit_saved',p,paths)
    p=old/'known_radius3_pair.json';d=json.loads(p.read_text());add(d,'M18_known_pair_fixture',p,[])
    return cases

def graph_of(c):return Graph(c['physical_edges'])
def vertices(x,n=7):return [v for v in range(n) if x>>v&1]
def dump_jsonl(name,rows):
    with (OUT/name).open('w',encoding='utf-8') as f:
        for r in rows:f.write(json.dumps(r,separators=(',',':'))+'\n')

def exact_cover(covers,full):
    """Exhaustive reachable-coverage DP; witnesses are shore masks."""
    dp={0:[]}
    for shore,bits in covers:
        for covered,choice in list(dp.items()):
            nxt=covered|bits
            if nxt not in dp or len(dp[nxt])>len(choice)+1:dp[nxt]=choice+[shore]
    if full not in dp:raise AssertionError('FAILURE_EXPLANATION_BUG')
    return dp[full]

def fiber_components(legal_states,internal_mask):
    """Independent small-fixture reference for the restricted physical fiber BFS."""
    groups={}
    for s in legal_states:groups.setdefault(s & ~internal_mask,set()).add(s)
    result={}
    for sig,group in groups.items():
        unseen=set(group);components=[]
        while unseen:
            start=min(unseen);unseen.remove(start);component={start};queue=[start]
            for s in queue:
                bits=internal_mask
                while bits:
                    bit=bits & -bits;bits-=bit;t=s^bit
                    if t in unseen:unseen.remove(t);component.add(t);queue.append(t)
            components.append(component)
        result[sig]=components
    return result
