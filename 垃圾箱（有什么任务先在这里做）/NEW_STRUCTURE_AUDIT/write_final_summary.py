import json,csv,collections,hashlib
from audit_core import *

def run():
    a=json.loads((OUT/'blocker_stats.json').read_text());d=json.loads((OUT/'tau_stats.json').read_text());b=json.loads((OUT/'phase_stats.json').read_text());c=json.loads((OUT/'leaf_stats.json').read_text())
    graphrows=list(csv.DictReader((OUT/'leaf_graph_results.csv').open()))
    fibers=list(csv.DictReader((OUT/'leaf_fiber_results.csv').open()))
    assert len(graphrows)==72 and len({(r['M'],r['graph_class']) for r in graphrows})==72
    assert collections.Counter(r['M'] for r in graphrows)=={'18':33,'19':1,'20':38}
    assert all(r['coverage']=='EXACT_COMPLETE_FOR_GRAPH' for r in graphrows)
    assert all(int(r['internal_edges'])==0 and int(r['fiber_size'])==1 for r in fibers)
    assert sum(int(r['number_of_fibers']) for r in fibers)==c['singleton_fibers']
    for r in graphrows:
        historical=list(csv.DictReader((ROOT/f"m{r['M']}_results/per_graph.csv").open()))
        original=next(x for x in historical if x['graph_class_index']==r['graph_class'])
        assert int(original['legal_orientation_count'])==int(r['legal_states'])
    total_states=sum(int(r['legal_states']) for r in graphrows)
    taudata=list(csv.DictReader((OUT/'tau_results.csv').open()))
    by_dataset={}
    for ds in sorted({r['dataset'] for r in taudata}):
        rr=[r for r in taudata if r['dataset']==ds];counts=collections.Counter(int(r['tau']) for r in rr if r['status']=='ALL_RECHARGES_FAIL')
        by_dataset[ds]=dict(cases=len(rr),all_fail=sum(counts.values()),one_step_success=sum(r['status']=='ONE_STEP_SUCCESS' for r in rr),empty=sum(r['status']=='EMPTY_RECHARGE_SET' for r in rr),tau_counts=dict(counts))
    provenance=[]
    inputs={ROOT/'m18_complete_hard_search.cpp'}
    for m in (18,19,20):inputs.update([ROOT/f'm{m}_results/records.jsonl',ROOT/f'm{m}_results/per_graph.csv'])
    inputs.update(Path(x['origin']) for x in saved_pairs())
    for p in sorted(inputs):provenance.append(dict(path=str(p),bytes=p.stat().st_size,sha256=hashlib.sha256(p.read_bytes()).hexdigest()))
    dump_jsonl('input_provenance.jsonl',provenance)
    (OUT/'output_validation.json').write_text(json.dumps(dict(status='PASS',graph_count=72,enumerated_legal_states=total_states,all_graph_counts_match_historical_csv=True,all_leaf_internal_edge_counts_zero=True,all_fibers_singleton=True,tau_by_dataset=by_dataset),indent=2))
    text=f'''# FINAL_SUMMARY

## 1. DATA INVENTORY

**SAVED WITNESSES ONLY** — A/D使用304个不同physical graph/source/target records：M18 saved d5 100条；M19 saved d7 100/216条（class1888）；M20 saved d7 100/13,404条（class1750）；3个旧explicit saved pairs与1个known-pair fixture。副本按physical edge list/source/target去重。fixture不假定Hamming=3。

**EXACT FOR LISTED GRAPH CLASSES** — C完整枚举72个classes的全部{total_states:,}个legal physical orientations：M18 32个max5 classes加class360（旧fixture），M19 class1888，M20全部38个max7 classes。原generator checksum分别372、8210、75701；hard38包含1750。所有legal counts与历史per_graph.csv逐class相符。class lists见reconstructed_hard_graphs.jsonl；标签EXACT_COMPLETE_FOR_GRAPH仅用于这些实际完成的classes。

**SAVED WITNESSES ONLY** — B有309条保存路径：303条shortest progress paths、3条shortest first-correction paths、3条source-target shortest paths。其中300条census paths均为progress paths，终点是首次Hamming<=2，不能解释为target。known-pair fixture没有saved path，未重建。

**INSUFFICIENT RAW DATA** — OLD-E1/Type-C1813、aw2、path-width3、harmful-blocker-birth、verified F-core H缺失；未猜映射、target或H，未运行FCORE_VARIANT。M19缺116条d7 raw pairs，M20缺13,304条；未补跑pair census。

**EXACT COMPLETE** — 本轮六组Python regression全部通过，覆盖原要求六项检查，并检验exact set-cover DP和internal-only fiber限制；C++ legality/slow-check/critical-phase fixture regression通过。日志见regression_results.txt、regression_cpp_results.txt。output_validation.json的最终覆盖/计数核对PASS。

## 2. BLOCKER CUT SIZE

**SAVED WITNESSES ONLY** — 915个blocked mismatch pair-edge occurrences：

|minimal cut size|次数|
|---|---:|
|5|821|
|6|94|
|>=7|0|

最大observed minimal cut size=6。全部blocker occurrences的cut-size分布：5有1640次，6有268次，>=7有0次。没有size>=7 certificate；JSONL保留解释记录。所有blocker families使用全部126个nonempty proper subsets，未root-normalize；每个交集都重新验证为tight blocker。

**PARTIAL** — `all canonical/minimal transient blockers have cut size 6`: **NOT ESTABLISHED**。这里只检查saved pairs；原规范可选A4的M20 hard38 all-state blocked-edge统计未执行。C的完整state枚举只用于fiber检查，不能扩充A的覆盖声明。

## 3. PHASE SKELETON

**EXACT FOR LISTED GRAPH CLASSES** — C的72个canonical graphs全部通过root0-normalized 5-cut laminarity检查。

**SAVED WITNESSES ONLY** — B分析8个explicit physical edge-list graph representations及309条paths；inclusion tree与root0不属于shore的约定均保存。1,934次physical legal flips全部通过phase-toggle invariant；每次至少跨一个critical shore，共4,652次shore toggles（平均每flip {4652/1934:.3f}）。这是saved-path验证，不是所有graphs的所有legal flips验证。

**SAVED WITNESSES ONLY** — 全部309条paths都存在某个critical shore重复toggle；200条saved d7 progress paths全部如此。完全无critical参与的hard path/纯transient episode：本批未观察到。

**SAVED WITNESSES ONLY** — 66个`3→4→3→2`片段的COMMON recharge都改变critical phases，且没有移除当前blocked mismatches的transient tight blockers；其中32个同时birth了transient blocker。因此`CRITICAL_ONLY`分类仅指“critical toggle、无transient blocker removal”，不代表noncritical cuts完全不变。例证见recharge_motif_examples.jsonl，全部shore变化见phase_path_traces.jsonl。仅描述数据，不升级为一般结论。

## 4. LEAF FIBER CONNECTIVITY

**EXACT FOR LISTED GRAPH CLASSES** —

|项目|数量|
|---|---:|
|exact complete graph classes|72|
|leaf critical shores（graph-leaf occurrences）|325|
|size>=2 fibers|0|
|connected size>=2 fibers|0|
|disconnected fibers|0|
|singleton fibers（均connected）|12,324,104|

本批全部leaf shores没有internal physical edges。每个outside signature固定所有edges，所以fiber size恰为1；完整legal enumeration后按这一确定事实输出singleton计数。leaf_fiber_results.csv把相同size=1的signatures汇总，number_of_fibers给精确数量，不列重复的一千多万行。**这批检查没有测试任何非平凡fiber，不能视为非平凡leaf-fiber connectivity的支持证据。** 没有counterexample，leaf_fiber_counterexamples.jsonl保留范围说明。

## 5. TWO-WITNESS TAU

**SAVED WITNESSES ONLY** — 只统计ALL_RECHARGES_FAIL：

|项目|数量|
|---|---:|
|case数（pair-edge）|623|
|tau=1|168|
|tau=2|455|
|tau>=3|0|
|maximum tau|2|

另外ONE_STEP_SUCCESS=292，EMPTY_RECHARGE_SET=0，均不计入tau。exact minimum cover采用穷尽reachable-coverage DP；所有SURVIVAL/BIRTH candidate shores来自全部proper subsets，每条失败recharge都有解释。输出含每case的minimum cover；没有tau>=3 certificate，JSONL保留no-certificate说明。

**SAVED WITNESSES ONLY** — **NO COUNTEREXAMPLE IN TESTED DATA**。这不是tau<=2 theorem。

## 6. COMPUTATIONAL VERDICT

- **SAVED WITNESSES ONLY**：A没有观察到minimal cut>=7；D没有观察到tau>=3；B没有观察到无critical transport的hard path。
- **EXACT FOR LISTED GRAPH CLASSES**：C完成72个classes的state universe；全部fibers为singleton，非平凡fiber测试数为0。
- **PARTIAL**：未恢复M19/M20全d7 pair集合，未执行可选A4全state blocker统计；不对缺失部分作negative结论。
- **INSUFFICIENT RAW DATA**：指定的旧1813 cases及其它命名raw datasets/F-core仍不可用。

没有M21/M22运行，没有progress-distance或pair census重算，没有一般定理或额外研究任务。所有新代码、输出与日志在NEW_STRUCTURE_AUDIT；历史文件只读。输入hash见input_provenance.jsonl。
'''
    (OUT/'FINAL_SUMMARY.md').write_text(text,encoding='utf-8')
    print('FINAL_SUMMARY written; output validation PASS; enumerated states',total_states)

if __name__=='__main__':run()
