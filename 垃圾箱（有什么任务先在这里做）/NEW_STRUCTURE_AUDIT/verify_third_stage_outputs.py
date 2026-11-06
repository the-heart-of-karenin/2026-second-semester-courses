"""Check third-stage artifacts/certificates without repeating census or regression."""
import json,csv,collections,hashlib
from pathlib import Path
from audit_core import OUT,ROOT,Graph

def run():
    for r in [json.loads(x) for x in (OUT/'input_provenance.jsonl').read_text().splitlines()]:
        assert hashlib.sha256(Path(r['path']).read_bytes()).hexdigest()==r['sha256']
    old=list(csv.DictReader((OUT/'all_state_blocker_size_per_graph.csv').open()));depth=list(csv.DictReader((OUT/'m20_hard38_blocker_depth_per_graph.csv').open()))
    assert len(depth)==38 and len({r['graph_class'] for r in depth})==38
    for r in depth[:2]:
        original=next(x for x in old if x['M']=='20' and x['graph_class']==r['graph_class'])
        for k in ['legal_states','blocked_edge_occurrences','cut5','cut6','cut7plus','maximum','histogram']:assert r[k]==original[k]
        assert r['source']=='REUSED_COMPLETED_CLASS'
    assert all(r['source']=='NEW_BLOCKER_DEPTH_TEST' for r in depth[2:])
    verified=[];previous=6
    for x in (OUT/'blocker_depth_record_certificates.jsonl').read_text().splitlines():
        r=json.loads(x);g=Graph(r['physical_edges']);s,e=r['orientation'],r['blocked_edge'];a,b=g.minimal(s,e)
        assert g.legal(s) and not g.legal(s^(1<<e))
        assert a==r['minimal_blocker'] and b==r['all_blockers'] and g.cuts[a][2]==r['cut_size']
        assert g.out(s,a)==r['out_cut']==2 and g.out(s,127^a)==r['in_cut']
        assert r['cut_size']>previous;previous=r['cut_size']
        verified.append(dict(graph_class=r['graph_class'],orientation=s,edge=e,cut=r['cut_size'],minimal_shore=a,independent_verification='PASS'))
    assert previous==json.loads((OUT/'m20_hard38_blocker_depth_histogram.json').read_text())['maximum']
    oldfib=list(csv.DictReader((OUT/'active_critical_fiber_results.csv').open()));newfib=list(csv.DictReader((OUT/'all_active_fiber_results.csv').open()))
    assert sum(r['source']=='REUSED_MINIMAL_ACTIVE_RESULT' for r in newfib)==64
    for r in newfib:
        if r['source']!='REUSED_MINIMAL_ACTIVE_RESULT':continue
        previousrow=next(x for x in oldfib if x['M']==r['M'] and x['graph_class']==r['graph_class'] and x['minimal_active_shore']==r['shore'])
        for k in ['fibers','nontrivial_fibers','max_fiber_size','connected_nontrivial_fibers','disconnected_nontrivial_fibers','internal_edges']:assert r[k]==previousrow[k]
    graphs=[json.loads(x) for x in (OUT/'reconstructed_hard_graphs.jsonl').read_text().splitlines() if json.loads(x)['M'] in (19,20)]
    allshore=list(csv.DictReader((OUT/'all_active_critical_shores.csv').open()))
    for r in graphs:
        edges=[uv for uv,m in zip([(u,v) for u in range(7) for v in range(u+1,7)],r['multiplicities']) for _ in range(m)]
        g=Graph(edges);sh,parent=g.skeleton();rows=[x for x in allshore if int(x['M'])==r['M'] and int(x['graph_class'])==r['graph_class']]
        assert sorted(int(x['shore']) for x in rows)==sorted(sh)
        active={a:sum(bool(a>>u&1 and a>>v&1) for u,v in edges) for a in sh}
        for x in rows:
            a=int(x['shore']);assert int(x['parent_shore'])==parent[a]
            d=0;p=a
            while p!=127:d+=1;p=parent[p]
            desc=sum(bool(active[b] and a!=b and a&b==b) for b in sh);anc=sum(bool(active[b] and a!=b and a&b==a) for b in sh)
            assert int(x['tree_depth'])==d and int(x['internal_edges'])==active[a] and int(x['active_descendants'])==desc and int(x['active_ancestors'])==anc
    (OUT/'third_stage_validation.json').write_text(json.dumps(dict(status='PASS',historical_inputs_unchanged=True,first_two_depth_aggregates_reused=True,all64_minimal_active_results_reused_exactly=True,all39_shore_hierarchies_verified=True,record_certificates=verified),indent=2))
    print('THIRD_STAGE_OUTPUT_VALIDATION PASS',verified)
if __name__=='__main__':run()
