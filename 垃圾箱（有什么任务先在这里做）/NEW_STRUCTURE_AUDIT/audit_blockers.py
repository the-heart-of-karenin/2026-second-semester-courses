import csv,collections,json
from audit_core import *

def run():
    counts=collections.Counter();datasets=collections.defaultdict(collections.Counter);allcounts=collections.Counter();deep=[];rows=[]
    for c in saved_pairs():
        g=graph_of(c);s=c['source'];t=c['target'];assert g.legal(s) and g.legal(t)
        for e in range(g.M):
            if not (s^t)>>e&1 or g.legal(s^(1<<e)):continue
            a,b=g.minimal(s,e);cut=g.cuts[a][2];category='CRITICAL_5' if cut==5 else 'SHALLOW_TRANSIENT_6' if cut==6 else 'DEEP_TRANSIENT_7PLUS'
            counts[cut]+=1;datasets[c['dataset']][cut]+=1;allcounts.update(g.cuts[x][2] for x in b);u,v=g.arc(s,e)
            row=dict(dataset=c['dataset'],coverage=c['coverage'],graph_class=c['graph_class'],source_state_id=s,target_state_id=t,edge_id=e,tail=u,head=v,blocker_count=len(b),minimal_blocker_mask=a,minimal_blocker_vertex_set=json.dumps(vertices(a)),minimal_blocker_cut_size=cut,classification=category,all_blocker_cut_sizes=json.dumps([g.cuts[x][2] for x in b]))
            rows.append(row)
            if cut>=7:deep.append(dict(**row,physical_edges=c['physical_edges'],all_blocker_masks=b,lambda_G=g.lam))
    with (OUT/'blocker_cut_sizes.csv').open('w',newline='',encoding='utf-8') as f:
        w=csv.DictWriter(f,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)
    deep.sort(key=lambda d:(len(d['physical_edges']),d['minimal_blocker_cut_size'],d['minimal_blocker_mask'],d['source_state_id'],d['target_state_id'],d['edge_id']))
    dump_jsonl('blocker_deep_certificates.jsonl',deep[:1] if deep else [dict(record_type='no_certificate',reason='No minimal blocker cut size >=7 observed',coverage='SAVED_WITNESSES_ONLY')])
    result=dict(pair_count=len(saved_pairs()),blocked_mismatch_rows=len(rows),minimal_cut_sizes=dict(counts),all_blocker_occurrences=dict(allcounts),by_dataset={k:dict(v) for k,v in datasets.items()},coverage='SAVED_WITNESSES_ONLY',deep_certificate_count=len(deep))
    (OUT/'blocker_stats.json').write_text(json.dumps(result,indent=2))
    (OUT/'blocker_cut_size_summary.md').write_text('# Minimal blocker cut-size audit\n\nSAVED_WITNESSES_ONLY. Counts are pair-edge occurrences, not distinct orientations or shores.\n\n```json\n'+json.dumps(result,indent=2)+'\n```\n\n'+('Observed cut >=7; smallest listed certificate: blocker_deep_certificates.jsonl.\n' if deep else 'No minimal cut >=7 observed in saved pairs.\n')+'\nAll canonical/minimal transient blockers have cut size 6: NOT ESTABLISHED.\n\nM19 coverage100/216; M20 coverage100/13404. OLD-E1/Type-C1813 and named missing datasets: INSUFFICIENT_RAW_DATA. Optional A4 all-state blocked-edge statistics are not included; C enumerates full hard-graph state universes for leaf fibers only. Such an optional graph-level blocker audit would not require target-pair enumeration.\n',encoding='utf-8')
    print(json.dumps(result),flush=True)
if __name__=='__main__':run()
