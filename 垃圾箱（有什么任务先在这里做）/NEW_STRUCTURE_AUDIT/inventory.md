# Workspace inventory / schema audit

审计日期：2026-09-30。当前阶段：仅 inventory 与 schema audit。

没有运行 regression tests、A/D/C/B 结构分析、graph enumeration 或 census；没有修改历史数据或旧脚本。下文 COMPLETE 指现有输出的覆盖声明与行数一致，不代表本轮独立重算验证。

## 1. 检查范围与文件清单

递归检查当前课程 workspace、同级 hajimi、STEP1_CORRECTNESS_work、QED，并检查旧 README 明确指向的 D 盘输出目录。不是全磁盘搜索。当前课程 workspace 没有本研究的 graph/orientation 数据；QED 内同名 hajimi archive 内容是其它数学项目，没有发现本任务原始数据。

全部已发现文件的完整路径、格式、类别与覆盖备注见同目录 `inventory_files.csv`（7459个文件）。该清单包含 primary project、旧 Python 项目和 D 盘输出，方便逐文件定位。批量 task JSONL 不是 physical orientation-state files。大量旧task文件仅核对样本schema与checkpoint覆盖，没有逐行验证所有内容；清单中的generic coverage_note需结合本报告范围解释。

### 主数据文件：每个 M 分开解释

| M | 完整路径 | 格式 / 内容 | 覆盖 |
|---|---|---|---|
|18|C:\Users\HUAWEI\Desktop\CodexWorkspace\hajimi\m18_results\summary.txt|aggregate census|COMPLETE，372/372|
|18|C:\Users\HUAWEI\Desktop\CodexWorkspace\hajimi\m18_results\checkpoint.txt|恢复进度、保存计数|完成 checkpoint|
|18|C:\Users\HUAWEI\Desktop\CodexWorkspace\hajimi\m18_results\per_graph.csv|graph class aggregate|COMPLETE，372行|
|18|C:\Users\HUAWEI\Desktop\CodexWorkspace\hajimi\m18_results\records.jsonl|graph + physical pair + progress path|CAPPED，100条，全部d5|
|18|C:\Users\HUAWEI\Desktop\CodexWorkspace\hajimi\m18_results\best_witness.txt|单个最佳 witness|PARTIAL|
|19|C:\Users\HUAWEI\Desktop\CodexWorkspace\hajimi\m19_results\summary.txt|aggregate census|COMPLETE，8210/8210|
|19|C:\Users\HUAWEI\Desktop\CodexWorkspace\hajimi\m19_results\checkpoint.txt|恢复进度、保存计数|完成 checkpoint|
|19|C:\Users\HUAWEI\Desktop\CodexWorkspace\hajimi\m19_results\per_graph.csv|graph class aggregate|COMPLETE，8210行|
|19|C:\Users\HUAWEI\Desktop\CodexWorkspace\hajimi\m19_results\records.jsonl|graph + physical pair + progress path|CAPPED，300条，d3/d5/d7各100|
|19|C:\Users\HUAWEI\Desktop\CodexWorkspace\hajimi\m19_results\best_witness.txt|单个最佳 witness|PARTIAL|
|20|C:\Users\HUAWEI\Desktop\CodexWorkspace\hajimi\m20_results\summary.txt|aggregate census|COMPLETE，75701/75701|
|20|C:\Users\HUAWEI\Desktop\CodexWorkspace\hajimi\m20_results\checkpoint.txt|恢复进度、保存计数|完成 checkpoint|
|20|C:\Users\HUAWEI\Desktop\CodexWorkspace\hajimi\m20_results\per_graph.csv|graph class aggregate|COMPLETE，75701行|
|20|C:\Users\HUAWEI\Desktop\CodexWorkspace\hajimi\m20_results\records.jsonl|graph + physical pair + progress path|CAPPED，300条，d3/d5/d7各100|
|20|C:\Users\HUAWEI\Desktop\CodexWorkspace\hajimi\m20_results\best_witness.txt|单个最佳 witness|PARTIAL|

|M|total legal states|qualifying ordered pairs|distance histogram|maximum witnesses (aggregate)|
|---|---:|---:|---|---:|
|18|5,855,322|3,897,018|3:3,888,130; 5:8,888|8,888|
|19|327,822,940|182,369,190|3:181,428,442; 5:940,532; 7:216|216|
|20|7,526,411,290|3,313,114,400|3:3,295,172,958; 5:17,928,038; 7:13,404|13,404|

这些是完整 aggregate，不是完整 pair/state 列表。M18 已保存 d5 只涉及 classes 0,2,4；M19 已保存 d7 只涉及1888；M20 已保存 d7 只涉及1750。保存选择受发现顺序和每个 distance 上限100影响，不是随机代表性样本。

M18 `maximum_distance=5` 的32个 classes：

`0,2,4,7,31,32,33,58,59,60,61,64,65,83,91,103,109,112,116,137,139,141,142,193,199,203,241,252,294,301,341,364`

M19 `maximum_distance=7`：`1888`（1个）。

M20 `maximum_distance=7`：恰好38个，包含1750：

`1750,2209,2365,8735,10160,11912,13012,13017,13077,13078,13766,13874,14080,14863,18436,18529,19505,21917,22471,22504,22515,25103,36873,41415,41499,41689,43318,43338,43589,43637,43640,43682,45836,45958,46156,46872,49450,67202`

## 2. C++ 数据 schema 与可复用实现

主实现：`C:\Users\HUAWEI\Desktop\CodexWorkspace\hajimi\m18_complete_hard_search.cpp`。

CSV header：`graph_class_index,legal_orientation_count,qualifying_ordered_pair_count,maximum_distance,distance_histogram`。graph index 为从0开始的 canonical graph vector index。CSV 没有 multiplicities、physical edges 或 orientation bits。maximum_distance=0 表示没有 qualifying pair，不能解释为没有 legal states。

M19/M20 JSONL fields：`M,graph_class_index,degrees,multiplicities,multiplicity_pair_endpoints,physical_edges,source,target,initial_mismatch_edges,source_legal_neighbors,distance,path,final_mismatch_at_most_2`。M18 旧格式没有 M/degrees，其 M 可从 physical_edges 长度确认；n=7 由 engine 固定。不要统一加载时要求所有行都有新字段。

`multiplicities` 的21个坐标按 unordered pairs `(u,v),u<v` 的字典顺序排列；`multiplicity_pair_endpoints` 给对应 pair。`physical_edges` 每条 copy 单独占一个位置，edge ID 为0-based数组位置。重复 endpoints 不合并。orientation 的 bit e=0 表示 physical_edges[e] 第一端点到第二端点，bit e=1 表示反向。source/target/state 为整数 bit mask，不是 quotient coordinate。

`path` 是节点列表，含 `state,flipped_edge,mismatch,move,legal`；起点 flipped_edge=-1，move=START。其它 move 按 flip 前该 edge 是否与 target 相同分 COMMON/CORRECTION。

**distance 是 progress distance：BFS 从 source 到首次 Hamming(current,target)<=2 的 legal state；path 不是完整 source->target shortest path。** 记录保留 target，但 path 通常不以 target 结束。B 阶段可直接追踪这些 shortest progress paths，必须明确 endpoint 语义；需要完整 target path 时只能对已保存 pair 单独重建，不能沿用 distance 当作 target distance。

可复用函数：

- `init_tables`：pair顺序、63个互补代表cuts；现有代表取 bit0=1。
- `degree_sequences/build_permutations/canonical/enumerate_graphs`：全 graph classes；unique map 的字典顺序确定 class index。恢复 hard classes 不需要执行 pair census。
- `edge_connected_5`：无向cut精确检查。
- `Engine`：physical edges、cut bit masks、`check`、`slow_check`、`prepare`、physical xor neighbors。
- `prepare`：临时内存枚举全部2^M legal flags；历史输出没有完整持久化 legal[state] 文件。
- `slow_check`：直接126个nonempty proper subsets检查出cut。
- `scan_source`：3条 individually blocked mismatches、legal target、Hamming3的 ordered qualifying universe。
- `distance`：shortest progress BFS。
- `witness_json`：保存 cap=100/dist；best_witness 是单个纪录，不是全集。

新 audit 的无向mincut shore必须转为 root0不属于X（原C++互补约定不同）。A/D的directed blocker / one-slack families必须遍历全部nonempty proper subsets，不可只用root-normalized一半。

## 3. 已有 connectivity 输出与程序

|完整路径|对象 / 现有输出覆盖|
|---|---|
|C:\Users\HUAWEI\Desktop\CodexWorkspace\hajimi\m19_connectivity_search.cpp|physical legal-state enumeration + connectivity BFS；可复用|
|C:\Users\HUAWEI\Desktop\CodexWorkspace\hajimi\connectivity_m19_results\summary.txt|COMPLETE：8210/8210，connected_graphs=8210|
|C:\Users\HUAWEI\Desktop\CodexWorkspace\hajimi\hard7_m20_connectivity.cpp|CSV选择hard38 + physical legality + BFS；可复用恢复class逻辑|
|C:\Users\HUAWEI\Desktop\CodexWorkspace\hajimi\hard7_m20_connectivity_results\summary.txt|COMPLETE_FOR_LISTED_CLASSES：38/38，disconnected=0|
|C:\Users\HUAWEI\Desktop\CodexWorkspace\hajimi\hard7_m20_connectivity_results\per_graph_connectivity.csv|38个class的connectivity aggregate；没有全部states|
|C:\Users\HUAWEI\Desktop\CodexWorkspace\hajimi\hard7_connectivity.cpp|saved witness candidates上的physical BFS|
|C:\Users\HUAWEI\Desktop\CodexWorkspace\hajimi\connectivity_results.txt|2个saved candidate：M19class1888 legal/reached=32832；M20class1750 legal/reached=81728，均connected；不是全部M20 universe|
|C:\Users\HUAWEI\Desktop\CodexWorkspace\hajimi\counterexample.txt|明确DISCONNECTED=NO among saved candidates；不是反例certificate|
|C:\Users\HUAWEI\Desktop\CodexWorkspace\hajimi\m20_frozen_bundle_search.cpp|quotient BFS；不应拿quotient states当physical fiber states|
|C:\Users\HUAWEI\Desktop\CodexWorkspace\hajimi\frozen_bundle_m20_results\summary.txt|COMPLETE frozen-bundle检查75701/75701，counterexamples=0|
|C:\Users\HUAWEI\Desktop\CodexWorkspace\hajimi\quotient_connectivity_m20_results\summary.txt|COMPLETE quotient connectivity75701/75701，disconnected=0|

这些全图connectivity历史结果不回答新的“固定outside signature、仅internal edges可flip”的C任务。

build/run脚本、checkpoint、exe、lock的具体路径见清单。lock文件存在本身不能证明进程正在运行。exe不是raw graph/state数据。M21/M22和n8随机搜索文件已登记为OUT_OF_SCOPE，不运行或扩大分析。

## 4. 旧 Python 项目及 D 盘 raw 输出

项目根：`C:\Users\HUAWEI\Desktop\CodexWorkspace\STEP1_CORRECTNESS_work`。

已读 README.md、STEP1_5_REPORT.md、SEARCH_README.md、SEARCH_N6_README.md、n7_hard_obstruction\README.md，并核对核心函数、schema构造和JSON样本。报告中旧测试通过记录不替代本轮regression tests。

|完整路径|格式 / 可复用内容|覆盖|
|---|---|---|
|C:\Users\HUAWEI\Desktop\CodexWorkspace\STEP1_CORRECTNESS_work\reference.py|Python Graph/Orientation、all-subsets legality、physical neighbors/components|实现，可作为独立reference|
|C:\Users\HUAWEI\Desktop\CodexWorkspace\STEP1_CORRECTNESS_work\fastcore.py|Python cut bitmask、legal_bits、neighbors/components|实现，保留physical IDs|
|C:\Users\HUAWEI\Desktop\CodexWorkspace\STEP1_CORRECTNESS_work\test_reference.py|旧regression fixtures|本轮未运行|
|C:\Users\HUAWEI\Desktop\CodexWorkspace\STEP1_CORRECTNESS_work\test_fastcore.py|reference/fast对照|本轮未运行|
|C:\Users\HUAWEI\Desktop\CodexWorkspace\STEP1_CORRECTNESS_work\n7_hard_obstruction\n7_core.py|Graph7.legal_and_flips/neighbors、cut_data、analyze_pair|仅M18 degree(6,5,5,5,5,5,5)，不可直接用于M19/20|
|C:\Users\HUAWEI\Desktop\CodexWorkspace\STEP1_CORRECTNESS_work\n7_hard_obstruction\search_n7.py|targeted pair sampler、sqlite checkpoint schema|SAMPLED pair discovery|
|C:\Users\HUAWEI\Desktop\CodexWorkspace\STEP1_CORRECTNESS_work\n7_hard_obstruction\verify_witness.py|certificate验证|实现|
|C:\Users\HUAWEI\Desktop\CodexWorkspace\STEP1_CORRECTNESS_work\n7_hard_obstruction\known_radius3_pair.json|m/source/target fixture|1个pair，source108956，target154012，无path|
|C:\Users\HUAWEI\Desktop\CodexWorkspace\STEP1_CORRECTNESS_work\n7_hard_obstruction\smoke_record\candidates\111111000221201210001_06668_14628.json|graph/pair/path certificate|SAMPLED；source26216,target83496，progress3|
|C:\Users\HUAWEI\Desktop\CodexWorkspace\STEP1_CORRECTNESS_work\n7_hard_obstruction\smoke_record\candidates\111111000221201210001_26c7a_30c7a.json|graph/pair/path certificate|SAMPLED；source158842,target199802，progress3|
|D:\GraphOrientationSearch_n7_M18\candidates\321000010011011200212_2d189_2d549.json|graph/pair/path完整certificate|SAMPLED discovery；精确pair BFS|
|D:\GraphOrientationSearch_n7_M18\radius_ge_4\321000010011011200212_2d189_2d549.json|同pair证书副本|不是第二个independent case|
|D:\GraphOrientationSearch_n7_M18\best_record.json|同pair最佳纪录副本|不是完整pair collection|
|D:\GraphOrientationSearch_n7_M18\status.json|targeted_scan_complete，372 graphs done|graph coverage exact；pair coverage SAMPLED|
|D:\GraphOrientationSearch_n7_M18\checkpoint.sqlite|meta/graphs/records数据库|graph multiplicities与sampling metadata，非全部states|

D盘M18证书包含 schema=n7-hard-obstruction-v1，source184713,target185673，physical_edges、m、lambda、blocked_mismatch_edges、source_legal_neighbors；first_correction_path、first_below_initial_path、target_path三种不同终点路径。其 progress=5，target_distance=7，不能归为“M19/M20 d7”。存有sourcecomponent size/hash；仅disconnected时程序才保存全部source_component_states，本例disconnected=false，未存完整states。

注意旧JSON同时有 `M`（edge数）和 `m`（multiplicities）。PowerShell默认ConvertFrom-Json会因大小写重复key报错；必须用case-sensitive parser（Python json或PowerShell -AsHashtable），不能丢字段。bits字符串为整数的常规高位在左显示，edgeID仍是整数bit位置，不可把字符串最左端当edge0。

SQLite schema经search_n7.py核对：meta(key,value)；graphs(graph_key,m_json,status,sample_checksum,sampled_states,orientation_trials,screened_pairs,exact_pairs,certificate_files,completed_at)；records(pair_key,rank_json,certificate_file,disconnected)。本轮read-only SQLite连接遇到 unable to open database file，未改库/未repair/未启动coordinator；没有读取出表行统计。graph状态372来自status.json，而非未成功执行的SQL。

另找到：

- `D:\GraphOrientationSearch\checkpoint.json`：n5、k2、M13–18 layer_complete，status=complete；目录5502个文件。task JSONL记录m,M,lambda,minimum_cut_mask,ambient_states,legal_states,component_count,component_sizes；这些是quotient graph aggregate，不含physical pair/path。
- `D:\GraphOrientationSearch_n6\checkpoint.json`：n6、M15–20 layer_complete；M21 status=running/partial（历史checkpoint，不推断实时运行）。目录1750个文件。JSONL额外n,k,degree_sequence，仍是quotient aggregate。M21不分析。
- `D:\GraphOrientationSearch_n7_M18`：7个文件；完整路径已逐项登记。

## 5. 缺失与后续可执行范围

|任务 / 数据层|可以直接做什么|限制与标签|
|---|---|---|
|A1 / D：M18 saved hard|100条d5完整pair；旧fixture及3个不同pair certificates可去重后逐例检查|SAVED_WITNESSES_ONLY；不能称全部8888，也不能称OLD-E1 1813|
|A2 / D：M19 d7|100条class1888 saved pairs|SAVED_WITNESSES_ONLY；216全集未保存。现有确定性graph generator和scan_source可只针对1888恢复，但本轮未运行/未证明几分钟可完成|
|A3 / D：M20 d7|100条class1750 saved pairs|SAVED_WITNESSES_ONLY；不是全部13404，也不是覆盖38classes的pair集|
|A4 / C3：M20 hard38|CSV可精确选38，复用原canonicalization恢复graphs，再枚举各graph全部physical legal states|恢复后才能标EXACT_COMPLETE_FOR_GRAPH；没有现成持久化state表|
|C1：M18 hard graphs|CSV选32个max5classes；或先saved classes0,2,4；旧certgraphs另按multiplicities去重|不是OLD-E1完整class列表；全部state需重新逐graph枚举|
|C2：M19 d7 graph|唯一class1888可恢复完整graph/state universe|无需恢复所有216pairs就能做graph-level fibers|
|B：saved paths|M18d5、M19d7、M20d7 progress paths；旧cert有target和first-below paths|SAVED_WITNESSES_ONLY；明确progress endpoint；旧progress3 paths可检查3->4->3->2|
|F-core secondary tau|不做|INSUFFICIENT_RAW_DATA：没有明确经过验证的H数据|

以下名称经路径/文件名和内容检索未找到可明确关联的raw records或可靠定义/索引：OLD-E1 / Type-C 1813、aw2、path-width3、harmful-blocker-birth、F-core。均记 `INSUFFICIENT_RAW_DATA`。缺：具体graph multiplicities/physical edges、source、target、case membership或已验证H。没有target的命名case将来必须记NO_TARGET_AVAILABLE_FOR_TAU；当前不能凭generic witness猜这些名称的对应关系。

没有发现完整M19 216或M20 13404 d7 pair文件；没有发现持久化全部legal physical states。找得到生成代码不等于已经恢复了raw data。没有对缺失集合给出negative结论。`all canonical/minimal transient blockers have cut size 6` 当前 `NOT ESTABLISHED`。

## 6. 下一阶段边界

先在NEW_STRUCTURE_AUDIT内添加独立regression tests：physical-ID保留、out+in=cut、slow/fast legality对照、flip/path连续性、blocker交集验证、root0补集约定。通过后依次A、D、C、B。优先cheap saved witnesses；graph-level恢复只限列出的M18hard/M19class1888/M20hard38。不要运行旧launcher或整个pair census。新增分析代码与全部输出仅写本audit目录。

本文件是inventory/schema结论，不是A/D/C/B计算结果，也没有宣称two-witness、leaf-fiber或phase的任何数学结论。
