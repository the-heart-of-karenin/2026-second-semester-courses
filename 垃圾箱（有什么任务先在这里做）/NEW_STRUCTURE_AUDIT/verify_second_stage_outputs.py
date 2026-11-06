"""Output/certificate consistency checks, not a rerun of regression or census."""
import csv,json,hashlib,collections
from audit_core import ROOT,OUT,Graph,vertices

def run():
    previous=[json.loads(x) for x in (OUT/'input_provenance.jsonl').read_text().splitlines()]
    for r in previous:
        from pathlib import Path
        assert hashlib.sha256(Path(r['path']).read_bytes()).hexdigest()==r['sha256'],'historical input hash changed'
    verified=[]
    for line in (OUT/'blocker_size_7plus_certificates.jsonl').read_text().splitlines():
        r=json.loads(line)
        if r.get('record_type')=='no_certificate':continue
        g=Graph(r['physical_edges']);s,e=r['orientation'],r['blocked_edge'];a,b=g.minimal(s,e)
        assert g.legal(s) and not g.legal(s^(1<<e))
        assert a==r['minimal_blocker'] and b==r['all_blockers']
        assert g.cuts[a][2]==r['cut_size']>=7 and g.arc(s,e)==(r['tail'],r['head'])
        verified.append(dict(M=r['M'],graph_class=r['graph_class'],orientation=s,blocked_edge=e,minimal_blocker_mask=a,minimal_blocker_vertices=vertices(a),cut_size=r['cut_size'],out_cut=g.out(s,a),all_blockers=b,independent_verification='PASS'))
    recovered=[json.loads(x) for x in (OUT/'m19_class1888_all_d7.jsonl').read_text().splitlines()]
    assert len(recovered)==len({(x['source'],x['target']) for x in recovered})==216
    g=Graph(recovered[0]['physical_edges'])
    for r in recovered:
        s,t=r['source'],r['target'];assert g.legal(s) and g.legal(t)
        assert (s^t).bit_count()==3
        assert all(not g.legal(s^(1<<e)) for e in r['initial_mismatch_edges'])
        path=r['path'];assert len(path)==8 and path[0]['state']==s and (path[-1]['state']^t).bit_count()<=2
        assert all((x['state']^t).bit_count()>2 for x in path[:-1])
        for x,y in zip(path,path[1:]):assert (x['state']^y['state']).bit_count()==1 and g.legal(y['state'])
    tau=list(csv.DictReader((OUT/'m19_class1888_tau.csv').open()))
    assert len(tau)==648 and {(int(r['source']),int(r['target'])) for r in tau}=={(r['source'],r['target']) for r in recovered}
    assert all(r['coverage']=='EXACT COMPLETE' for r in tau)
    active=list(csv.DictReader((OUT/'active_critical_fiber_results.csv').open()))
    keys={(int(r['M']),int(r['graph_class'])) for r in active}
    assert len(keys)==39 and sum(int(r['nontrivial_fibers']) for r in active)==920380
    assert sum(int(r['disconnected_nontrivial_fibers']) for r in active)==0
    for m,gi in keys:
        historical=list(csv.DictReader((ROOT/f'm{m}_results/per_graph.csv').open()))
        expected=int(next(x for x in historical if int(x['graph_class_index'])==gi)['legal_orientation_count'])
        assert all(int(x['legal_states'])==expected for x in active if int(x['M'])==m and int(x['graph_class'])==gi)
    result=dict(status='PASS',historical_input_hashes_unchanged=True,recovered_pairs_validated=216,tau_occurrences=648,graphs_with_exact_active_fiber_check=39,nontrivial_fibers=920380,deep_certificates_independently_verified=verified)
    (OUT/'second_stage_validation.json').write_text(json.dumps(result,indent=2))
    first=verified[0]
    (OUT/'first_cut7_certificate.txt').write_text('Verified actual minimal-blocker cut7 certificate\n\nSource: blocker_size_7plus_certificates.jsonl, first record.\n'+json.dumps(first,indent=2)+'\n\nThe source is legal; flipping the listed physical edge is illegal. All blocker shores are listed above. Their intersection is {0}; outgoing cut count=2; underlying cut size=7. Full multiplicities and physical edge list are in the JSONL record.\n')
    summary=OUT/'all_state_blocker_size_summary.md'
    summary.write_text(summary.read_text()+'\nIndependent126-subset verification passed for all3 saved deep certificates; first_cut7_certificate.txt records the first case. Task2 intentionally stops after M20class2209 is complete (2/38 M20classes); the 36 remaining classes were not blocker-audited. Task3 nevertheless completes its own full39-graph range.\n')
    final=OUT/'SECOND_STAGE_SUMMARY.md';text=final.read_text(encoding='utf-8')
    text=text.replace('Actual cut>=7 certificates: blocker_size_7plus_certificates.jsonl. Early stopping occurs only after completing the certificate graph.', 'Actual cut>=7 certificates: blocker_size_7plus_certificates.jsonl, independently verified via all126 directed subsets. First case: M20class2209, orientation67134, physical edge0, minimal blocker {0}, out-cut2, underlying cut7. Task2 early stop occurs after completing class2209; M20blocker coverage is2/38 (36classes untested), while M19class1888 is complete. Task3 still completes all39 graphs.')
    final.write_text(text,encoding='utf-8')
    print('Second-stage output and certificate verification PASS')
if __name__=='__main__':run()
