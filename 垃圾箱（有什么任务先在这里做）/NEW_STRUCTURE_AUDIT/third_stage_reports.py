import csv,json,collections,sys
from audit_core import ROOT,OUT,Graph,dump_jsonl,vertices

def profile():
    pairs=[json.loads(x) for x in (OUT/'m19_class1888_all_d7.jsonl').read_text().splitlines()]
    edges=list(csv.DictReader((OUT/'m19_class1888_tau.csv').open()));group=collections.defaultdict(list)
    for r in edges:group[(int(r['graph_class']),int(r['source']),int(r['target']))].append(r)
    if len(pairs)!=216 or len(group)!=216 or len(edges)!=648:raise RuntimeError('TAU_PROFILE_INPUT_INCONSISTENCY')
    g=Graph(pairs[0]['physical_edges']);hist=collections.Counter();statistics={1:collections.defaultdict(collections.Counter),2:collections.defaultdict(collections.Counter)};result=[];exceptions={}
    for p in pairs:
        key=(1888,p['source'],p['target']);rows=group[key];ids=sorted(p['initial_mismatch_edges'])
        if len(rows)!=3 or sorted(int(r['blocked_edge']) for r in rows)!=ids or len(set(int(r['blocked_edge']) for r in rows))!=3 or any(r['status']!='ALL_RECHARGES_FAIL' or not r['tau'] for r in rows):raise RuntimeError('TAU_PROFILE_INPUT_INCONSISTENCY')
        rows.sort(key=lambda r:int(r['blocked_edge']));values=[int(r['tau']) for r in rows];prof=tuple(sorted(values));hist[prof]+=1
        s=p['source'];degree=collections.Counter(g.arc(s,e)[0] for e in range(g.M));details=[]
        for r in rows:
            e=int(r['blocked_edge']);tau=int(r['tau']);R=json.loads(r['recharge_edges']);B=g.family(s,e,2);N=g.family(s,e,3);a,_=g.minimal(s,e);u,v=g.arc(s,e)
            for name,value in [('R_size',len(R)),('B_e_size',len(B)),('N_e_size',len(N)),('minimal_blocker_cut_size',g.cuts[a][2]),('directed_edge_endpoints',f'{u}->{v}'),('tail_outdegree',degree[u]),('head_outdegree',degree[v])]:statistics[tau][name][value]+=1
            details.append(dict(edge_id=e,tau=tau,R_size=len(R),minimum_witness_cover=json.loads(r['minimum_cover'])))
        result.append(dict(graph_class=1888,source=p['source'],target=p['target'],mismatch_edge_ids=json.dumps(ids),tau_in_edge_id_order=json.dumps(values),sorted_profile=json.dumps(prof),R_sizes=json.dumps([x['R_size'] for x in details]),minimum_witness_covers=json.dumps([x['minimum_witness_cover'] for x in details]),coverage='EXACT COMPLETE'))
        if prof!=(1,2,2):exceptions.setdefault(prof,dict(graph_class=1888,source=p['source'],target=p['target'],profile=prof,physical_edges=p['physical_edges'],mismatches=details))
    with (OUT/'m19_d7_tau_profiles.csv').open('w',newline='') as f:
        w=csv.DictWriter(f,fieldnames=list(result[0]));w.writeheader();w.writerows(result)
    dump_jsonl('tau_profile_exceptions.jsonl',exceptions.values() if exceptions else [dict(record_type='no_exception',reason='All216 profiles are (1,2,2)',coverage='EXACT COMPLETE')])
    data=dict(distinct_ordered_pairs=216,expected=216,total_edge_records=648,profile_histogram={str(k):v for k,v in sorted(hist.items())},all_216_have_profile_1_2_2=not exceptions,cheap_histograms={str(t):{name:dict(v) for name,v in dd.items()} for t,dd in statistics.items()})
    (OUT/'m19_d7_tau_profile_stats.json').write_text(json.dumps(data,indent=2))
    text='distinct ordered pairs = 216\nexpected = 216\n\nprofile histogram:\n'+''.join(f'    {p}: {n}\n' for p,n in sorted(hist.items()))+'\nALL_216_HAVE_PROFILE_1_2_2 = '+('YES' if not exceptions else 'NO')+'\n\nEXACT COMPLETE finite-layer pattern.\n\nStable identifier: (graph_class,source,target); exactly3 distinct physical mismatch edge records per pair; total648. Tau values/minimum covers are read from previous exact audit, not recomputed.\n\nCheap per-tau histograms (pair-edge occurrences):\n```json\n'+json.dumps(data['cheap_histograms'],indent=2)+'\n```\n'
    (OUT/'m19_d7_tau_profile_summary.md').write_text(text)
    print('TAU PROFILES',data['profile_histogram'],flush=True)

def prepare():
    # Keep all previous implementations unchanged; include them without their old main.
    source=(OUT/'second_stage.cpp').read_text();prefix=source[:source.index('int main(int argc,char**argv)try{')]
    (OUT/'third_stage_shared.inc').write_text(prefix)
    graphs=[json.loads(x) for x in (OUT/'reconstructed_hard_graphs.jsonl').read_text().splitlines() if json.loads(x)['M'] in (19,20)]
    assert len(graphs)==39
    with (OUT/'third_graph_multiplicities.txt').open('w') as f:
        for r in graphs:f.write(str(r['M'])+' '+str(r['graph_class'])+' '+' '.join(map(str,r['multiplicities']))+'\n')
    old=list(csv.DictReader((OUT/'all_state_blocker_size_per_graph.csv').open()))
    selected=[r for r in old if r['M']=='20'];assert [int(r['graph_class']) for r in selected]==[1750,2209]
    with (OUT/'m20_depth_seed.txt').open('w') as f:
        for r in selected:f.write(','.join(r[x] for x in ['M','graph_class','legal_states','blocked_edge_occurrences','cut5','cut6','cut7plus','maximum'])+',"'+r['histogram']+'",REUSED_COMPLETED_CLASS\n')
    records=[json.loads(x) for x in (OUT/'blocker_size_7plus_certificates.jsonl').read_text().splitlines()];r=next(x for x in records if x.get('cut_size')==7)
    g=Graph(r['physical_edges']);a=r['minimal_blocker'];r.update(minimal_blocker_vertex_set=vertices(a),out_cut=g.out(r['orientation'],a),in_cut=g.out(r['orientation'],127^a),origin='REUSED_EARLIER_GLOBAL_RECORD',previous_maximum=6)
    if not (OUT/'blocker_depth_record_certificates.jsonl').exists():dump_jsonl('blocker_depth_record_certificates.jsonl',[r])
    reuse=list(csv.DictReader((OUT/'active_critical_fiber_results.csv').open()))
    assert len(reuse)==64
    with (OUT/'minimal_active_reuse.txt').open('w') as f:
        for r in reuse:f.write(' '.join(r[k] for k in ['M','graph_class','minimal_active_shore','internal_edges','fibers','nontrivial_fibers','max_fiber_size','connected_nontrivial_fibers','disconnected_nontrivial_fibers'])+'\n')

def depth():
    rows=list(csv.DictReader((OUT/'m20_hard38_blocker_depth_per_graph.csv').open()));assert len(rows)==38
    hist=collections.Counter()
    for r in rows:
        assert int(r['legal_states'])==int(next(x for x in csv.DictReader((ROOT/'m20_results/per_graph.csv').open()) if x['graph_class_index']==r['graph_class'])['legal_orientation_count'])
        for item in r['histogram'].split(';'):
            size,count=map(int,item.split(':'));hist[size]+=count
    maximum=max(hist);classes=[int(r['graph_class']) for r in rows if int(r['maximum'])==maximum]
    data=dict(completed_classes=38,expected_classes=38,total_legal_states=sum(int(r['legal_states']) for r in rows),total_blocked_edge_occurrences=sum(int(r['blocked_edge_occurrences']) for r in rows),histogram={str(k):hist.get(k,0) for k in range(5,maximum+1)},maximum=maximum,maximum_graph_classes=classes,maximum_occurrence_count=hist[maximum],coverage='EXACT FOR M20 HARD38 GRAPH CLASSES')
    (OUT/'m20_hard38_blocker_depth_histogram.json').write_text(json.dumps(data,indent=2))
    (OUT/'m20_hard38_blocker_depth_summary.md').write_text('coverage: EXACT FOR M20 HARD38 GRAPH CLASSES\n\ncompleted classes / 38 = 38/38\n\n```json\n'+json.dumps(data,indent=2)+'\n```\n\n1750 and2209 reuse completed aggregates; the remaining36 classes were checked. All126 directed proper subsets are scanned and all legal physical state-edge occurrences checked. No target pairs used. Newly generated canonical multiplicities are checked against reconstructed_hard_graphs.jsonl and legal counts against historical CSV. Per-graph checkpoint saved. Record certificates only: blocker_depth_record_certificates.jsonl; first retained record7 comes from previous verified class2209. No general bound claimed.\n')
    print('BLOCKER DEPTH',json.dumps(data),flush=True)

def fibers():
    rows=list(csv.DictReader((OUT/'all_active_fiber_results.csv').open()));sh=list(csv.DictReader((OUT/'all_active_critical_shores.csv').open()))
    assert len({(r['M'],r['graph_class']) for r in sh})==39
    depth=collections.defaultdict(collections.Counter)
    for r in rows:
        d=int(r['tree_depth']);depth[d]['active_shores']+=1
        for k in ['fibers','nontrivial_fibers','connected_nontrivial_fibers','disconnected_nontrivial_fibers']:depth[d][k]+=int(r[k])
    data=dict(graphs_processed=39,total_critical_shores=len(sh),active_proper_critical_shores=len(rows),minimal_active_reused=sum(r['source']=='REUSED_MINIMAL_ACTIVE_RESULT' for r in rows),non_minimal_active_newly_tested=sum(r['source']=='NEW_ALL_ACTIVE_TEST' for r in rows),total_fibers=sum(int(r['fibers']) for r in rows),nontrivial_fibers=sum(int(r['nontrivial_fibers']) for r in rows),maximum_fiber_size=max(int(r['max_fiber_size']) for r in rows),connected_nontrivial_fibers=sum(int(r['connected_nontrivial_fibers']) for r in rows),disconnected_nontrivial_fibers=sum(int(r['disconnected_nontrivial_fibers']) for r in rows),tree_depth_histogram={str(k):dict(v) for k,v in sorted(depth.items())},coverage='EXACT FOR LISTED GRAPH CLASSES')
    if data['disconnected_nontrivial_fibers']:
        certs=[json.loads(x) for x in (OUT/'all_active_fiber_counterexamples.jsonl').read_text().splitlines() if json.loads(x).get('record_type')!='no_certificate']
        certs.sort(key=lambda r:(r['shore_size'],r['fiber_size'],r['graph_class'],r['M'],r['shore'],r['outside_signature']))
        dump_jsonl('all_active_fiber_smallest_certificate.jsonl',[certs[0]])
        title='ALL-ACTIVE CRITICAL FIBER CONNECTIVITY FALSE\non tested exact graph universe'
    else:title='NO COUNTEREXAMPLE IN EXACT 39-GRAPH UNIVERSE'
    (OUT/'all_active_fiber_stats.json').write_text(json.dumps(data,indent=2))
    (OUT/'all_active_fiber_summary.md').write_text(title+'\n\ncoverage: EXACT FOR LISTED GRAPH CLASSES\n\n```json\n'+json.dumps(data,indent=2)+'\n```\n\nRoot0 absent from shores; V is not a critical shore. Depth(root V)=0. Ancestor/descendant counts use proper inclusion and active shores only. Reused minimal-active results are marked separately and receive no new BFS. All new shores use complete legal physical state tables, exact outside signatures and internal-only BFS. Counts are graph-shore-fiber occurrences; nested shores may contain the same physical state.\n')
    print('ALL ACTIVE',json.dumps(data),flush=True)

def final():
    p=json.loads((OUT/'m19_d7_tau_profile_stats.json').read_text());b=json.loads((OUT/'m20_hard38_blocker_depth_histogram.json').read_text());f=json.loads((OUT/'all_active_fiber_stats.json').read_text())
    text='# THIRD_STAGE_SUMMARY\n\n## 1. M19 COMPLETE TAU PROFILE\n\ncoverage: EXACT COMPLETE\n\nIs every one of the216 d7 pairs profile(1,2,2)? **'+('YES' if p['all_216_have_profile_1_2_2'] else 'NO')+'**\n\nProfile histogram:\n```json\n'+json.dumps(p['profile_histogram'],indent=2)+'\n```\n216 distinct ordered pairs; each has3 physical mismatch records; total648. Exact complete finite-layer pattern. Cheap histograms: m19_d7_tau_profile_summary.md.\n'
    text+='\n## 2. M20 HARD38 BLOCKER DEPTH\n\ncoverage: EXACT FOR M20 HARD38 GRAPH CLASSES\n\nmaximum observed |delta(A_e)| = **'+str(b['maximum'])+'**\n\n```json\n'+json.dumps(b,indent=2)+'\n```\n\nRecord certificates: blocker_depth_record_certificates.jsonl. First2 classes reused; remaining36 completed.\n'
    text+='\n## 3. ALL-ACTIVE CRITICAL FIBERS\n\ncoverage: EXACT FOR LISTED GRAPH CLASSES\n\nAny disconnected nontrivial fiber? **'+('YES' if f['disconnected_nontrivial_fibers'] else 'NO')+'**\n\n```json\n'+json.dumps(f,indent=2)+'\n```\n\n'+('Smallest counterexample: all_active_fiber_smallest_certificate.jsonl.\n' if f['disconnected_nontrivial_fibers'] else 'No counterexample in exact39-graph universe.\n')
    text+='\nQ1 = '+('YES' if p['all_216_have_profile_1_2_2'] else 'NO')+'\nQ2 = '+str(b['maximum'])+'\nQ3 = '+('YES' if f['disconnected_nontrivial_fibers'] else 'NO')+'\n'
    (OUT/'THIRD_STAGE_SUMMARY.md').write_text(text,encoding='utf-8')
    print('THIRD_STAGE COMPLETE',flush=True)
if __name__=='__main__':globals()[sys.argv[1]]()
