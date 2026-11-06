import csv,collections,json
from audit_core import *

def run():
    rows=[];certs=[];statuses=collections.Counter();taus=collections.Counter()
    for c in saved_pairs():
        g=graph_of(c);s,t=c['source'],c['target'];assert g.legal(s) and g.legal(t)
        R=[e for e in range(g.M) if not (s^t)>>e&1 and g.legal(s^(1<<e))]
        for e in range(g.M):
            if not (s^t)>>e&1 or g.legal(s^(1<<e)):continue
            base=dict(dataset=c['dataset'],coverage=c['coverage'],graph_class=c['graph_class'],source=s,target=t,blocked_edge=e,recharge_edges=json.dumps(R),status='',tau='',minimum_cover='')
            if not R:base['status']='EMPTY_RECHARGE_SET'
            else:
                success=[r for r in R if g.legal(s^(1<<r)^(1<<e))]
                if success:base['status']='ONE_STEP_SUCCESS';base['successful_recharges']=json.dumps(success)
                else:
                    B=g.family(s,e,2);Ns=g.family(s,e,3);covers=[];details=[]
                    for x in B+Ns:
                        covered=[]
                        for i,r in enumerate(R):
                            a,b=g.arc(s,r);enter=not x>>a&1 and x>>b&1;leave=x>>a&1 and not x>>b&1
                            if x in B:assert not leave
                            explains=(x in B and not enter) or (x in Ns and leave)
                            if explains:covered.append(i)
                        bits=sum(1<<i for i in covered);covers.append((x,bits));details.append(dict(shore=x,type='SURVIVAL' if x in B else 'BIRTH',explains=[R[i] for i in covered]))
                    full=(1<<len(R))-1;union=0
                    for _,b in covers:union|=b
                    assert union==full,'FAILURE_EXPLANATION_BUG'
                    cover=exact_cover(covers,full);tau=len(cover);base.update(status='ALL_RECHARGES_FAIL',tau=tau,minimum_cover=json.dumps(cover));taus[tau]+=1
                    if tau>=3:certs.append(dict(**base,physical_edges=c['physical_edges'],lambda_G=g.lam,B_e=B,N_e=Ns,witness_coverage=details,exact_minimum_cover=cover,exact_algorithm='exhaustive reachable-coverage DP over all candidate shores'))
            statuses[base['status']]+=1;rows.append(base)
    fields=['dataset','coverage','graph_class','source','target','blocked_edge','recharge_edges','status','tau','minimum_cover','successful_recharges']
    with (OUT/'tau_results.csv').open('w',newline='',encoding='utf-8') as f:
        w=csv.DictWriter(f,fieldnames=fields);w.writeheader();w.writerows(rows)
    dump_jsonl('tau_counterexamples.jsonl',certs if certs else [dict(record_type='no_certificate',status='NO COUNTEREXAMPLE IN TESTED DATA',coverage='SAVED_WITNESSES_ONLY',missing_datasets='INSUFFICIENT_RAW_DATA')])
    stats=dict(statuses=dict(statuses),tau_counts=dict(taus),all_recharges_fail_cases=sum(taus.values()),maximum_tau=max(taus,default=None),counterexamples=len(certs),coverage='SAVED_WITNESSES_ONLY')
    (OUT/'tau_stats.json').write_text(json.dumps(stats,indent=2))
    title='TWO_WITNESS CONJECTURE FALSE ON TESTED INSTANCE' if certs else 'NO COUNTEREXAMPLE IN TESTED DATA'
    (OUT/'tau_summary.md').write_text(title+'\n\nSAVED_WITNESSES_ONLY; primary R only. EMPTY_RECHARGE_SET and ONE_STEP_SUCCESS are excluded from tau counts.\n\n```json\n'+json.dumps(stats,indent=2)+'\n```\n\nNamed missing raw datasets and verified F-core H: INSUFFICIENT_RAW_DATA; FCORE_VARIANT skipped. No guessed targets or H.\n')
    print(json.dumps(stats),flush=True)
if __name__=='__main__':run()
