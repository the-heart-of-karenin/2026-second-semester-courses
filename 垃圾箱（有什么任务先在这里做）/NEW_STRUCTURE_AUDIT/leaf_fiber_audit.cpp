// Include the verified generator and physical legality engine without invoking its pair search.
#define main historical_census_main_not_called
#include "../m18_complete_hard_search.cpp"
#undef main
#include <set>

struct Selected { int index; uint64_t expected; };
std::vector<Selected> selected(int m) {
    std::ifstream f(fs::path(ROOT)/("m"+std::to_string(m)+"_results")/"per_graph.csv");
    std::string line; std::getline(f,line);
    if(line!="graph_class_index,legal_orientation_count,qualifying_ordered_pair_count,maximum_distance,distance_histogram")throw std::runtime_error("CSV schema mismatch");
    std::vector<Selected> result;
    while(std::getline(f,line)) {
        std::stringstream ss(line);std::string a,b,c,d;
        std::getline(ss,a,',');std::getline(ss,b,',');std::getline(ss,c,',');std::getline(ss,d,',');
        if(std::stoi(d)==(m==18?5:7))result.push_back({std::stoi(a),std::stoull(b)});
    }
    if(result.size()!=size_t(m==18?32:m==19?1:38))throw std::runtime_error("hard selection checksum");
    if(m==20 && std::none_of(result.begin(),result.end(),[](auto x){return x.index==1750;}))throw std::runtime_error("missing1750");
    return result;
}
int outgoing(const Engine &e,U s,int x) {
    int o=0;for(int i=0;i<M;++i){auto [u,v]=e.edges[i];if(s>>i&1)std::swap(u,v);o+=(x>>u&1)&&!(x>>v&1);}return o;
}
int cutsize(const Engine &e,int x){int c=0;for(auto p:e.edges)c+=((x>>p.u)^(x>>p.v))&1;return c;}
std::vector<int> shores(const Engine &e) {
    std::vector<int> r;for(int x=1;x<127;++x)if(!(x&1)&&cutsize(e,x)==5)r.push_back(x);
    for(int x:r)for(int y:r)if((x&y)&&((x&y)!=x)&&((x&y)!=y))throw std::runtime_error("ODD_MINCUT_LAMINARITY_FAILURE");
    return r;
}
std::string ints(const std::vector<U>&v){std::ostringstream f;f<<'[';for(size_t i=0;i<v.size();++i){if(i)f<<',';f<<v[i];}f<<']';return f.str();}
std::string phase(const Engine &e,U s,const std::vector<int>& sh){std::ostringstream f;f<<'[';for(size_t i=0;i<sh.size();++i){if(i)f<<',';int o=outgoing(e,s,sh[i]);if(o!=2&&o!=3)throw std::runtime_error("phase failure");f<<o;}f<<']';return f.str();}

void certificate(std::ofstream &f,const Engine &e,int gi,int leaf,U signature,const std::vector<U>&states,const std::vector<U>&sizes,const std::vector<U>&reps,const std::vector<int>&sh,U internal) {
    f<<"{\"record_type\":\"counterexample\",\"M\":"<<M<<",\"graph_class\":"<<gi<<",\"leaf\":"<<leaf<<",\"outside_signature\":"<<signature<<",\"internal_edge_mask\":"<<internal<<",\"fiber_size\":"<<states.size()<<",\"component_sizes\":"<<ints(sizes)<<",\"representatives\":"<<ints(reps)<<",\"physical_edges\":[";
    for(int i=0;i<M;++i){if(i)f<<',';f<<'['<<e.edges[i].u<<','<<e.edges[i].v<<']';}f<<"],\"multiplicities\":[";
    for(int i=0;i<21;++i){if(i)f<<',';f<<int(e.graph[i]);}
    f<<"],\"states_with_critical_phase\":[";
    for(size_t i=0;i<states.size();++i){if(i)f<<',';U s=states[i];f<<"{\"state\":"<<s<<",\"outdegrees_on_critical_shores\":"<<phase(e,s,sh)<<",\"blocked_internal_flips\":[";bool first=true;
        for(int id=0;id<M;++id)if(internal>>id&1 && !e.legal[s^(1u<<id)]) {
            if(!first)f<<',';first=false;auto [u,v]=e.edges[id];if(s>>id&1)std::swap(u,v);std::vector<U>b;
            for(int x=1;x<127;++x)if((x>>u&1)&&!(x>>v&1)&&outgoing(e,s,x)==2)b.push_back(x);
            if(b.empty())throw std::runtime_error("missing internal blocker");f<<"{\"edge\":"<<id<<",\"blockers\":"<<ints(b)<<'}';
        }f<<"]}";
    }f<<"],\"critical_shores\":[";for(size_t i=0;i<sh.size();++i){if(i)f<<',';f<<sh[i];}f<<"],\"coverage\":\"EXACT_COMPLETE_FOR_GRAPH\"}\n";f.flush();
}

int main(int argc,char **argv)try {
    fs::path out=fs::absolute(argv[0]).parent_path();
    if(argc==2 && std::string(argv[1])=="--self-test") {
        init_tables();M=19;S=1u<<M;
        // Saved class1888 multiplicities supplied through independent fixture file.
        std::ifstream in(out/"regression_graph.txt");Graph g{};int n;for(auto &x:g){if(!(in>>n))throw std::runtime_error("fixture missing");x=uint8_t(n);}Engine e(g);
        e.prepare(1);if(e.legal_count!=32832)throw std::runtime_error("legal-count regression");
        for(U s=0;s<S;++s)if(s%997==0&&e.check(s)!=e.slow_check(s))throw std::runtime_error("legality reference mismatch");
        auto sh=shores(e);for(U s=0;s<S;++s)if(e.legal[s])for(int x:sh){int a=outgoing(e,s,x);if(a!=2&&a!=3)throw std::runtime_error("critical phase");}
        std::cout<<"C++ legality/critical-shore regression PASS; legal=32832\n";return 0;
    }
    std::ofstream summary(out/"leaf_graph_results.csv"), fibers(out/"leaf_fiber_results.csv"),cert(out/"leaf_fiber_counterexamples.jsonl"),graphs(out/"reconstructed_hard_graphs.jsonl");
    summary<<"M,graph_class,legal_states,leaf_count,nontrivial_fibers,connected_nontrivial_fibers,disconnected_fibers,coverage\n";
    fibers<<"M,graph_class,leaf_mask,internal_edges,outside_signature,fiber_size,component_count,component_sizes,number_of_fibers,coverage\n";
    uint64_t graph_total=0,leaf_total=0,nontrivial=0,connected=0,disconnected=0,singletons=0;
    init_tables();auto hw=std::thread::hardware_concurrency();unsigned workers=hw>2?hw-2:1;
    for(int m:{18,19,20}) {
        M=m;S=1u<<M;auto en=enumerate_graphs();if(en.classes.size()!=size_t(m==18?372:m==19?8210:75701))throw std::runtime_error("enumeration checksum");
        auto sel=selected(m);
        // M18 old saved certificate graphs may lie outside max5; explicitly include them.
        if(m==18){std::ifstream extras(out/"extra_m18_graphs.txt");Graph g{};int val;while(extras>>val){g[0]=uint8_t(val);for(int i=1;i<21;++i){if(!(extras>>val))throw std::runtime_error("extra graph fixture");g[i]=uint8_t(val);}g=canonical_unfixed(g);auto it=std::lower_bound(en.classes.begin(),en.classes.end(),g);if(it==en.classes.end()||*it!=g)throw std::runtime_error("old graph class not found");int idx=int(it-en.classes.begin());if(std::none_of(sel.begin(),sel.end(),[&](auto x){return x.index==idx;}))sel.push_back({idx,0});}}
        for(auto item:sel) {
            Engine e(en.classes.at(item.index));e.prepare(workers);if(item.expected&&e.legal_count!=item.expected)throw std::runtime_error("legal count differs from census");
            std::vector<U> states;states.reserve(e.legal_count);for(U s=0;s<S;++s)if(e.legal[s])states.push_back(s);
            auto sh=shores(e);std::vector<int>leaves;for(int x:sh)if(std::none_of(sh.begin(),sh.end(),[&](int y){return y!=x&&(x&y)==y;}))leaves.push_back(x);
            graphs<<"{\"M\":"<<M<<",\"graph_class\":"<<item.index<<",\"legal_states\":"<<e.legal_count<<",\"multiplicities\":[";for(int i=0;i<21;++i){if(i)graphs<<',';graphs<<int(e.graph[i]);}graphs<<"],\"critical_shores\":[";for(size_t i=0;i<sh.size();++i){if(i)graphs<<',';graphs<<sh[i];}graphs<<"],\"leaf_shores\":[";for(size_t i=0;i<leaves.size();++i){if(i)graphs<<',';graphs<<leaves[i];}graphs<<"]}\n";
            uint64_t nt=0,co=0,di=0;
            for(int leaf:leaves) {
                ++leaf_total;U internal=0;std::vector<int>ids;
                for(int id=0;id<M;++id)if((leaf>>e.edges[id].u&1)&&(leaf>>e.edges[id].v&1)){internal|=1u<<id;ids.push_back(id);}
                if(!internal){singletons+=states.size();fibers<<M<<','<<item.index<<','<<leaf<<",0,ALL_SIGNATURES,1,1,\"[1]\","<<states.size()<<",EXACT_COMPLETE_FOR_GRAPH\n";continue;}
                std::map<U,std::vector<U>> groups;for(U s:states)groups[s&~internal].push_back(s);
                std::vector<uint8_t> seen(S,0);std::vector<U>queue;queue.reserve(states.size());
                uint64_t single=0;
                for(auto &[signature,group]:groups) {
                    if(group.size()==1){++single;continue;}++nt;
                    std::vector<U>sizes,reps;
                    for(U start:group)if(!seen[start]){queue.clear();queue.push_back(start);seen[start]=1;reps.push_back(start);
                        for(size_t head=0;head<queue.size();++head)for(int id:ids){U t=queue[head]^(1u<<id);if(e.legal[t]&&!seen[t]){if((t&~internal)!=signature)throw std::runtime_error("fiber signature changed");seen[t]=1;queue.push_back(t);}}
                        sizes.push_back(U(queue.size()));
                    }
                    uint64_t reached=std::accumulate(sizes.begin(),sizes.end(),uint64_t(0));if(reached!=group.size())throw std::runtime_error("fiber coverage mismatch");
                    fibers<<M<<','<<item.index<<','<<leaf<<','<<ids.size()<<','<<signature<<','<<group.size()<<','<<sizes.size()<<",\""<<ints(sizes)<<"\",1,EXACT_COMPLETE_FOR_GRAPH\n";
                    if(sizes.size()>1){++di;certificate(cert,e,item.index,leaf,signature,group,sizes,reps,sh,internal);}else ++co;
                }
                singletons+=single;if(single)fibers<<M<<','<<item.index<<','<<leaf<<','<<ids.size()<<",SINGLETON_SIGNATURES,1,1,\"[1]\","<<single<<",EXACT_COMPLETE_FOR_GRAPH\n";
            }
            ++graph_total;nontrivial+=nt;connected+=co;disconnected+=di;
            summary<<M<<','<<item.index<<','<<e.legal_count<<','<<leaves.size()<<','<<nt<<','<<co<<','<<di<<",EXACT_COMPLETE_FOR_GRAPH\n";summary.flush();fibers.flush();graphs.flush();
            std::cout<<"M="<<M<<" class="<<item.index<<" legal="<<e.legal_count<<" leaves="<<leaves.size()<<" nontrivial_fibers="<<nt<<" disconnected="<<di<<std::endl;
        }
    }
    if(!disconnected)cert<<"{\"record_type\":\"no_certificate\",\"status\":\"NO COUNTEREXAMPLE IN TESTED DATA\",\"coverage\":\"EXACT FOR LISTED GRAPH CLASSES\"}\n";
    std::ofstream stats(out/"leaf_stats.json");stats<<"{\"graphs\":"<<graph_total<<",\"leaves\":"<<leaf_total<<",\"nontrivial_fibers\":"<<nontrivial<<",\"connected_nontrivial_fibers\":"<<connected<<",\"disconnected_fibers\":"<<disconnected<<",\"singleton_fibers\":"<<singletons<<"}\n";
    return 0;
} catch(const std::exception &e){std::cerr<<"ERROR: "<<e.what()<<std::endl;return 1;}
