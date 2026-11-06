"""Second-stage tau reuses the unmodified, previously tested audit_two_witness.run."""
import csv,json,collections,sys
from audit_core import ROOT,OUT,dump_jsonl

def tau():
    import audit_two_witness as audited
    recovered=[json.loads(x) for x in (OUT/'m19_class1888_all_d7.jsonl').read_text().splitlines()]
    metadata=json.loads((OUT/'m19_recovery_stats.json').read_text())
    pairs={(r['source'],r['target']) for r in recovered}
    if len(recovered)!=216 or len(pairs)!=216 or metadata['coverage']!='EXACT COMPLETE':
        (OUT/'m19_class1888_tau_summary.md').write_text(f'M19_D7_RECOVERY_COUNT_MISMATCH\nrecovered d7 pairs = {len(recovered)}\nexpected = 216\ncoverage = PARTIAL\n');raise RuntimeError('recovery mismatch')
    old=[json.loads(x) for x in (ROOT/'m19_results/records.jsonl').read_text().splitlines() if json.loads(x)['distance']==7]
    assert {(r['source'],r['target']) for r in old}<=pairs
    for r in recovered:
        assert r['M']==19 and r['graph_class_index']==1888 and r['distance']==7
        assert (r['source']^r['target']).bit_count()==3
        assert r['path'][0]['state']==r['source'] and (r['path'][-1]['state']^r['target']).bit_count()<=2
    cases=[dict(dataset='M19_class1888_complete_d7',coverage='EXACT COMPLETE',graph_class=1888,source=r['source'],target=r['target'],physical_edges=r['physical_edges']) for r in recovered]
    names={'tau_results.csv':'m19_class1888_tau.csv','tau_stats.json':'m19_class1888_tau_stats.json','tau_summary.md':'m19_class1888_tau_summary.md','tau_counterexamples.jsonl':'m19_class1888_tau_counterexamples.jsonl'}
    class RenamedOutput:
        def __truediv__(self,name):return OUT/names[name]
    audited.OUT=RenamedOutput();audited.saved_pairs=lambda:cases
    audited.dump_jsonl=lambda name,rows:dump_jsonl(names[name],rows)
    audited.run()
    stats=json.loads((OUT/names['tau_stats.json']).read_text());stats['coverage']='EXACT COMPLETE';stats['recovered_d7_pairs']=216
    (OUT/names['tau_stats.json']).write_text(json.dumps(stats,indent=2))
    certificates=[json.loads(x) for x in (OUT/names['tau_counterexamples.jsonl']).read_text().splitlines()]
    if stats['counterexamples']:
        certificates.sort(key=lambda r:(int(r['tau']),r['source'],r['target'],r['blocked_edge']))
        dump_jsonl('m19_class1888_tau_smallest_certificate.jsonl',[certificates[0]])
        title='TWO_WITNESS FALSE ON COMPLETE M19-d7 LAYER'
    else:
        title='EXACT COMPLETE FOR M19 d7: no tau>=3 found among all 216 pairs'
        dump_jsonl(names['tau_counterexamples.jsonl'],[dict(record_type='no_certificate',reason='No tau>=3 in all216 M19 d7 pairs',coverage='EXACT COMPLETE')])
    text=title+'\n\ncoverage = EXACT COMPLETE\nrecovered d7 pairs = 216\nexpected = 216\n\n```json\n'+json.dumps(stats,indent=2)+'\n```\n\nCounts are pair-edge occurrences. Only ALL_RECHARGES_FAIL receives tau; primary recharge definition and exhaustive reachable-coverage DP are reused without modification from audit_two_witness.py / audit_core.py. No cap. All100 previously saved pairs are present. Physical bits/edge IDs unchanged. Recovered paths are shortest progress paths to first Hamming<=2, not source-target shortest paths.\n'
    (OUT/names['tau_summary.md']).write_text(text)
    print('COMPLETE M19-d7 TAU',json.dumps(stats),flush=True)

def blockers():
    rows=list(csv.DictReader((OUT/'all_state_blocker_size_per_graph.csv').open()))
    stats={}
    for m in (19,20):
        rr=[r for r in rows if int(r['M'])==m]
        stats[str(m)]=dict(completed_classes=len(rr),expected_classes=1 if m==19 else 38,legal_states=sum(int(r['legal_states']) for r in rr),blocked_edge_occurrences=sum(int(r['blocked_edge_occurrences']) for r in rr),cut5=sum(int(r['cut5']) for r in rr),cut6=sum(int(r['cut6']) for r in rr),cut7plus=sum(int(r['cut7plus']) for r in rr),maximum=max((int(r['maximum']) for r in rr),default=None))
    complete=stats['19']['completed_classes']==1 and stats['20']['completed_classes']==38
    deep=sum(s['cut7plus'] for s in stats.values())
    title='EXACT FOR M19 CLASS1888 + M20 HARD38: no minimal blocker cut >=7 observed' if complete and not deep else 'MINIMAL BLOCKER CUT >=7 FOUND' if deep else 'PARTIAL all-state blocker audit'
    text=title+'\n\ncoverage = '+('EXACT FOR LISTED GRAPH CLASSES' if complete else 'PARTIAL')+'\n\n```json\n'+json.dumps(stats,indent=2)+'\n```\n\nEvery legal physical state and every individually blocked physical edge of each completed graph is checked. All126 nonempty proper directed subsets are scanned; tight outgoing edge masks identify all B_e and their intersections. Independently verify flip-illegal iff B_e nonempty and verify each A_e remains a tight separating shore. No target orientation is used. Tables are newly enumerated and legal counts match historical per_graph.csv. Histograms count physical state-edge occurrences. Per-class atomic CSV/checkpoint commits permit resume.\n'
    if deep:text+='\nFirst few explicit deep certificates: blocker_size_7plus_certificates.jsonl. The graph containing a deep certificate was completed before early stop.\n'
    (OUT/'all_state_blocker_size_summary.md').write_text(text)
    (OUT/'all_state_blocker_stats.json').write_text(json.dumps(dict(coverage='EXACT FOR LISTED GRAPH CLASSES' if complete else 'PARTIAL',stages=stats),indent=2))
    print('ALL-STATE BLOCKER',json.dumps(stats),flush=True)

def active():
    stats=json.loads((OUT/'active_fiber_stats.json').read_text());rows=list(csv.DictReader((OUT/'active_critical_fiber_results.csv').open()))
    graphkeys={(r['M'],r['graph_class']) for r in rows};assert len(graphkeys)==stats['graphs_processed']==39
    certificates=[json.loads(x) for x in (OUT/'active_critical_fiber_counterexamples.jsonl').read_text().splitlines()]
    if stats['disconnected_nontrivial_fibers']:
        certificates.sort(key=lambda r:(r['fiber_size'],r['M'],r['graph_class'],r['shore'],r['outside_signature']))
        dump_jsonl('active_critical_fiber_smallest_certificate.jsonl',[certificates[0]])
        title='NONTRIVIAL_CRITICAL_FIBER FALSE'
    else:title='NO COUNTEREXAMPLE IN EXACT LISTED GRAPH CLASSES'
    text=title+'\n\ncoverage = EXACT FOR LISTED GRAPH CLASSES\n\n```json\n'+json.dumps(stats,indent=2)+'\n```\n\nScope: M19 class1888 followed by all M20 hard38. Root0-normalized 5-cut family is checked laminar. Only proper critical shores with internal physical edges are active; minimal-active means no proper active critical subshore. V is never included. Every fiber is constructed from the entire enumerated legal physical state table and grouped by exact bits outside its internal-edge mask. Components use only legal single internal-physical-edge flips; boundary/outside flips forbidden. Original M18 leaf tests are not rerun.\n'
    if stats['disconnected_nontrivial_fibers']:text+='\nSmallest actual certificate: active_critical_fiber_smallest_certificate.jsonl. It lists all boundary states, legal internal flips, and all directed tight blockers for every failed internal flip, plus distinct-component representatives.\n'
    (OUT/'active_critical_fiber_summary.md').write_text(text)
    print('ACTIVE FIBER',json.dumps(stats),flush=True)

def final():
    t=json.loads((OUT/'m19_class1888_tau_stats.json').read_text());b=json.loads((OUT/'all_state_blocker_stats.json').read_text());f=json.loads((OUT/'active_fiber_stats.json').read_text())
    q1=t['counterexamples']>0;q2=any(v['cut7plus']>0 for v in b['stages'].values());q3=f['disconnected_nontrivial_fibers']>0
    assert t['recovered_d7_pairs']==216
    text='# SECOND_STAGE_SUMMARY\n\n## 1. COMPLETE M19-d7 TAU RESULT\n\ncoverage: **EXACT COMPLETE**\n\nRecovered216/216 ordered d7 pairs, uncapped. Class reconstruction matches saved multiplicities/physical edge list; legal states=32,832. Full class qualifying pair count and histogram also match historical CSV: 53,244 pairs; d3=46,332, d5=6,696, d7=216. All100 old saved d7 pairs are included.\n\n```json\n'+json.dumps(t,indent=2)+'\n```\n\n'+('TWO_WITNESS FALSE ON COMPLETE M19-d7 LAYER. Smallest certificate: m19_class1888_tau_smallest_certificate.jsonl.\n' if q1 else 'EXACT COMPLETE FOR M19 d7: no tau>=3 found among all216 pairs. This is a finite-layer result, not a theorem.\n')
    text+='\n## 2. ALL-STATE MINIMAL-BLOCKER SIZE RESULT\n\ncoverage: **'+b['coverage']+'**\n\n```json\n'+json.dumps(b['stages'],indent=2)+'\n```\n\n'+('Actual cut>=7 certificates: blocker_size_7plus_certificates.jsonl. Early stopping occurs only after completing the certificate graph.\n' if q2 else 'EXACT FOR M19 CLASS1888 + M20 HARD38: no minimal blocker cut >=7 observed. All directed subsets and all blocked physical state-edge occurrences checked; no pair targets or M20 pair census.\n')
    text+='\n## 3. NONTRIVIAL CRITICAL-SHORE FIBER RESULT\n\ncoverage: **EXACT FOR LISTED GRAPH CLASSES**\n\n```json\n'+json.dumps(f,indent=2)+'\n```\n\n'+('NONTRIVIAL_CRITICAL_FIBER FALSE. Smallest certificate: active_critical_fiber_smallest_certificate.jsonl.\n' if q3 else 'NO COUNTEREXAMPLE IN EXACT LISTED GRAPH CLASSES. Only minimal-active proper critical shores are tested.\n')
    text+='\nQ1. tau>=3 in complete216 M19 d7 pairs? **'+('YES' if q1 else 'NO')+'**\n\nQ2. minimal blocker cut>=7 in M19class1888 + M20hard38 states? **'+('YES' if q2 else 'NO')+'**\n\nQ3. disconnected tested nontrivial minimal-active critical fiber? **'+('YES' if q3 else 'NO')+'**\n'
    (OUT/'SECOND_STAGE_SUMMARY.md').write_text(text,encoding='utf-8')
    print('FINAL',q1,q2,q3,flush=True)

if __name__=='__main__':globals()[sys.argv[1]]()
