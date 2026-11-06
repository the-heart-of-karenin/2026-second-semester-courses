import collections,json
from audit_core import *

def run():
    traces=[];graph_info={};totals=collections.Counter();path_repeated=0;path_without_critical=0;recharge_types=collections.Counter();recharge_examples={};motif_transient_births=0
    for c in saved_pairs():
        g=graph_of(c);key=g.edges;sh,parent=g.skeleton()
        if key not in graph_info:graph_info[key]=dict(physical_edges=g.edges,lambda_G=g.lam,critical_shores=sh,inclusion_parent=parent,root=g.full,root_normalization='0 not in shore')
        source_blockers=[]
        for e in range(g.M):
            if (c['source']^c['target'])>>e&1 and not g.legal(c['source']^(1<<e)):
                a,b=g.minimal(c['source'],e);source_blockers.append(dict(edge=e,minimal_shore=a,minimal_cut_size=g.cuts[a][2],blocker_masks=b))
        for p in c['paths']:
            nodes=p['nodes'];steps=[];toggle_counts=collections.Counter();transport=0
            for a,b in zip(nodes,nodes[1:]):
                s,t=a['state'],b['state'];xor=s^t;assert xor.bit_count()==1;e=xor.bit_length()-1
                crossed=g.verify_flip(s,t,e);toggle_counts.update(crossed);transport+=len(crossed);totals['legal_flips_checked']+=1;totals['phase_toggles']+=len(crossed)
                if crossed:totals['flips_with_critical_transport']+=1
                u,v=g.arc(s,e);common=not (s^c['target'])>>e&1
                # A legal flip has no current blocker leaving its tail shore.
                assert not g.family(s,e,2)
                noncritical_tight_crossed=[x for x,(_,_,cut) in g.cuts.items() if cut>5 and bool(x>>u&1)!=bool(x>>v&1) and g.out(s,x)==2]
                noncritical_one_slack_leaving=[x for x,(_,_,cut) in g.cuts.items() if cut>5 and x>>u&1 and not x>>v&1 and g.out(s,x)==3]
                changes=[];removed_transient=False
                if common:
                    for mismatch in range(g.M):
                        if not (s^c['target'])>>mismatch&1 or g.legal(s^(1<<mismatch)):continue
                        before=set(g.family(s,mismatch,2));after=set(g.family(t,mismatch,2));removed=sorted(before-after);born=sorted(after-before)
                        if any(g.cuts[x][2]>5 for x in removed):removed_transient=True
                        changes.append(dict(mismatch_edge=mismatch,removed_blockers=[dict(shore=x,cut_size=g.cuts[x][2]) for x in removed],born_blockers=[dict(shore=x,cut_size=g.cuts[x][2]) for x in born],still_blocked=not g.legal(t^(1<<mismatch))))
                steps.append(dict(flipped_physical_edge=e,current_orientation_before=s,current_orientation_after=t,mismatch_before=(s^c['target']).bit_count(),mismatch_after=(t^c['target']).bit_count(),move='COMMON' if common else 'CORRECTION',crossed_critical_shores=crossed,before_phase_vector=g.phases(s),after_phase_vector=g.phases(t),phase_hamming_distance=len(crossed),currently_blocked_by_noncritical_cut=False,noncritical_tight_crossed_shores=noncritical_tight_crossed,noncritical_one_slack_leaving_shores=noncritical_one_slack_leaving,blocked_mismatch_family_changes=changes,removed_transient_blocker=removed_transient))
            motifs=[]
            for i in range(len(nodes)-3):
                mismatches=[(x['state']^c['target']).bit_count() for x in nodes[i:i+4]]
                if mismatches==[3,4,3,2]:
                    step=steps[i];critical=bool(step['crossed_critical_shores']);transient=step['removed_transient_blocker']
                    typ='BOTH_CRITICAL_AND_TRANSIENT' if critical and transient else 'CRITICAL_ONLY' if critical else 'TRANSIENT_ONLY' if transient else 'NEITHER_OBSERVED'
                    birth=any(z['cut_size']>5 for change in step['blocked_mismatch_family_changes'] for z in change['born_blockers'])
                    motif_transient_births+=birth
                    motifs.append(dict(start_step=i,recharge_classification=typ,classification_scope='critical toggles versus removed transient tight blockers; births listed separately',transient_blocker_birth=birth));recharge_types[typ]+=1
                    recharge_examples.setdefault(typ,dict(dataset=c['dataset'],source=c['source'],target=c['target'],path_kind=p['kind'],states=[x['state'] for x in nodes[i:i+4]],physical_edges=c['physical_edges'],common_step=step))
            repeats=[x for x,count in toggle_counts.items() if count>1]
            if repeats:path_repeated+=1
            if transport==0:path_without_critical+=1
            trace=dict(dataset=c['dataset'],coverage='SAVED_WITNESSES_ONLY',graph_class=c['graph_class'],physical_edges=c['physical_edges'],source=c['source'],target=c['target'],path_kind=p['kind'],is_source_target_shortest_path=p['kind']=='shortest_source_target_path',endpoint_condition='Hamming(state,target)<=2' if p['kind']=='shortest_progress_path' else 'first correction' if p['kind']=='shortest_first_correction_path' else 'state==target',reported_distance=p['reported_distance'],path_states=[n['state'] for n in nodes],steps=steps,critical_shores=sh,source_blocked_mismatches=source_blockers,repeatedly_toggled_shores=repeats,motifs_3_4_3_2=motifs)
            traces.append(trace)
    dump_jsonl('phase_path_traces.jsonl',traces);dump_jsonl('phase_skeletons.jsonl',graph_info.values());dump_jsonl('recharge_motif_examples.jsonl',recharge_examples.values())
    d7=[x for x in traces if x['dataset'] in ('M19_saved_hard','M20_saved_hard') and x['path_kind']=='shortest_progress_path']
    stats=dict(graph_representations=len(graph_info),hard_paths=len(traces),path_kind_counts=dict(collections.Counter(x['path_kind'] for x in traces)),laminarity_passed=True,phase_toggle_invariant_passed=True,**totals,paths_with_repeated_phase_toggle=path_repeated,d7_paths_with_repeated_phase_toggle=sum(bool(x['repeatedly_toggled_shores']) for x in d7),d7_path_count=len(d7),paths_with_zero_critical_transport=path_without_critical,recharge_3_4_3_2_classes=dict(recharge_types),motifs_with_transient_blocker_birth=motif_transient_births,purely_transient_hard_episode_observed=any(x['steps'] and all(not s['crossed_critical_shores'] for s in x['steps']) and any(s['removed_transient_blocker'] for s in x['steps']) for x in traces),coverage='SAVED_WITNESSES_ONLY')
    (OUT/'phase_stats.json').write_text(json.dumps(stats,indent=2))
    (OUT/'phase_path_summary.md').write_text('# Odd-mincut phase / hard-path traces\n\nSAVED_WITNESSES_ONLY. graph_representations counts exact labelled endpoint lists, not isomorphism classes.\n\n```json\n'+json.dumps(stats,indent=2)+'\n```\n\nThe 300 census paths are shortest progress paths, not source-target shortest paths. Older files separately supply first-correction, progress and complete source-target paths. Shortestness comes from the audited historical BFS; this audit verifies legality, physical edge IDs, consecutive flips and endpoint semantics, without re-running pair BFS.\n\nA legal flip has no current tight blocker that it leaves. Noncritical tight cuts crossed and one-slack cuts left are listed separately; neither is called a current illegal-flip blocker. Recharge classification uses observed removal of noncritical tight blockers on currently blocked mismatches, and critical phase changes, not an invented necessity criterion. Motif certificates are in recharge_motif_examples.jsonl. Counts describe saved data only.\n\nNamed missing paths: INSUFFICIENT_RAW_DATA. known_radius3_pair fixture has no saved path and is not included in path counts.\n')
    print(json.dumps(stats),flush=True)
if __name__=='__main__':run()
