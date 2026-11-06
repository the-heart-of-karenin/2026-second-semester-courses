#define main historical_census_main_not_called
#include "../m18_complete_hard_search.cpp"
#undef main
#include <set>
#include <limits>

namespace second {
fs::path out;
const std::vector<int> hard20={1750,2209,2365,8735,10160,11912,13012,13017,13077,13078,13766,13874,14080,14863,18436,18529,19505,21917,22471,22504,22515,25103,36873,41415,41499,41689,43318,43338,43589,43637,43640,43682,45836,45958,46156,46872,49450,67202};
unsigned workers(){auto n=std::thread::hardware_concurrency();return n>2?n-2:1;}
struct Historical {uint64_t legal=0,pair_count=0;Counts hist;};
Historical historical(int m,int gi){
    std::ifstream f(fs::path(ROOT)/("m"+std::to_string(m)+"_results")/"per_graph.csv");std::string line;std::getline(f,line);
    if(line!="graph_class_index,legal_orientation_count,qualifying_ordered_pair_count,maximum_distance,distance_histogram")throw std::runtime_error("historical CSV schema");
    std::set<int> d7;Historical result;
    while(std::getline(f,line)){std::stringstream s(line);std::string a,b,c,d,h;std::getline(s,a,',');std::getline(s,b,',');std::getline(s,c,',');std::getline(s,d,',');std::getline(s,h);if(h.size()>1&&h.front()=='"'&&h.back()=='"')h=h.substr(1,h.size()-2);
        int id=std::stoi(a);if(std::stoi(d)==7)d7.insert(id);if(id==gi)result={std::stoull(b),std::stoull(c),parse_hist(h)};
    }
    std::set<int> expected=m==19?std::set<int>{1888}:std::set<int>(hard20.begin(),hard20.end());
    if(d7!=expected||!result.legal)throw std::runtime_error("hard graph list mismatch");return result;
}
std::string vector_json(const std::vector<U>&v){std::ostringstream f;f<<'[';for(size_t i=0;i<v.size();++i){if(i)f<<',';f<<v[i];}f<<']';return f.str();}
std::string graph_json(const Engine&e){std::ostringstream f;f<<"\"multiplicities\":[";for(int i=0;i<21;++i){if(i)f<<',';f<<int(e.graph[i]);}f<<"],\"physical_edges\":[";for(int i=0;i<M;++i){if(i)f<<',';f<<'['<<e.edges[i].u<<','<<e.edges[i].v<<']';}f<<']';return f.str();}
struct AllCuts {
    std::array<CutInfo,127> cut{};
    explicit AllCuts(const Engine&e){for(int x=1;x<127;++x)for(int id=0;id<M;++id){auto [u,v]=e.edges[id];if(((x>>u)^(x>>v))&1){auto &c=cut[x];c.crossing|=1u<<id;++c.total;if(x>>u&1)c.zero_out|=1u<<id;else c.one_out|=1u<<id;}}}
    U outgoing(U s,int x)const{return (~s&cut[x].zero_out)|(s&cut[x].one_out);}
    std::vector<U> blockers(U s,int edge)const{std::vector<U>b;for(int x=1;x<127;++x){U o=outgoing(s,x);if((o>>edge&1)&&std::popcount(o)==2)b.push_back(x);}return b;}
    std::vector<int> shores()const{std::vector<int>s;for(int x=1;x<127;++x)if(!(x&1)&&cut[x].total==5)s.push_back(x);for(int x:s)for(int y:s)if((x&y)&&(x&y)!=x&&(x&y)!=y)throw std::runtime_error("MINCUT_LAMINARITY_BUG");return s;}
};
void save_table(const Engine&e,int gi){auto p=out/("legal_M"+std::to_string(M)+"_class"+std::to_string(gi)+".bin");std::ofstream f(p,std::ios::binary);f.write(reinterpret_cast<const char*>(e.legal.data()),S);if(!f)throw std::runtime_error("legal table write");}
void load_table(Engine&e,int gi){auto p=out/("legal_M"+std::to_string(M)+"_class"+std::to_string(gi)+".bin");std::ifstream f(p,std::ios::binary);if(!f||fs::file_size(p)!=S)throw std::runtime_error("missing verified legal table");f.read(reinterpret_cast<char*>(e.legal.data()),S);if(!f)throw std::runtime_error("legal table read");for(auto x:e.legal){if(x>1)throw std::runtime_error("corrupt legal table");e.legal_count+=x;}if(e.legal_count!=historical(M,gi).legal)throw std::runtime_error("legal count mismatch");}

void recover(){
    M=19;S=1u<<M;init_tables();auto en=enumerate_graphs();if(en.classes.size()!=8210)throw std::runtime_error("CLASS_RECONSTRUCTION_MISMATCH");
    Engine master(en.classes.at(1888));auto expected=historical(19,1888);
    std::ifstream fixture(out/"m19_reconstruction_fixture.txt");int value;
    for(int i=0;i<21;++i)if(!(fixture>>value)||value!=master.graph[i])throw std::runtime_error("CLASS_RECONSTRUCTION_MISMATCH multiplicities");
    for(auto edge:master.edges){int u,v;if(!(fixture>>u>>v)||u!=edge.u||v!=edge.v)throw std::runtime_error("CLASS_RECONSTRUCTION_MISMATCH physical edges");}
    master.prepare(workers());if(master.legal_count!=expected.legal)throw std::runtime_error("CLASS_RECONSTRUCTION_MISMATCH legal count");save_table(master,1888);
    std::vector<U> sources;for(U s=0;s<S;++s)if(master.legal[s])sources.push_back(s);
    auto start=std::chrono::steady_clock::now();std::atomic<size_t>next{0},finished{0};std::atomic<bool>abort{false};std::mutex mutex;std::exception_ptr failure;
    struct Record{U source,target;std::array<int,3>mis;std::vector<U>path;};std::vector<Record> records;Counts hist;uint64_t total=0;
    unsigned nw=workers();std::vector<std::thread>threads;
    for(unsigned i=0;i<nw;++i)threads.emplace_back([&]{try{Engine engine(master.graph);engine.legal=master.legal;engine.legal_count=master.legal_count;engine.queue.reserve(master.legal_count);Counts local;uint64_t pc=0;std::vector<Record> rec;
        while(!abort){size_t k=next.fetch_add(1);if(k>=sources.size())break;
            scan_source(engine,sources[k],[&](U s,U t,const std::array<int,3>&mis,int d){++pc;++local[d];if(d==7){std::vector<U>path;if(engine.distance(s,t,true,&path)!=7)throw std::runtime_error("BFS distance mismatch");rec.push_back({s,t,mis,std::move(path)});}});
            auto done=finished.fetch_add(1)+1;if(done%4096==0){std::lock_guard<std::mutex>lock(mutex);std::cout<<"class1888 sources "<<done<<'/'<<sources.size()<<std::endl;}
        }
        std::lock_guard<std::mutex>lock(mutex);total+=pc;for(auto [d,c]:local)hist[d]+=c;records.insert(records.end(),rec.begin(),rec.end());
    }catch(...){abort=true;std::lock_guard<std::mutex>lock(mutex);if(!failure)failure=std::current_exception();}});
    for(auto &t:threads)t.join();if(failure)std::rethrow_exception(failure);
    std::sort(records.begin(),records.end(),[](const auto&a,const auto&b){return std::tie(a.source,a.target)<std::tie(b.source,b.target);});
    std::ofstream f(out/"m19_class1888_all_d7.jsonl");for(auto&r:records)f<<witness_json(1888,master,r.source,r.target,r.mis,7,r.path)<<'\n';f.close();
    Counts cleaned;for(auto [d,c]:expected.hist)if(c)cleaned[d]=c;
    double sec=std::chrono::duration<double>(std::chrono::steady_clock::now()-start).count();
    std::ostringstream status;status<<"{\"recovered_d7_pairs\":"<<records.size()<<",\"expected\":216,\"legal_states\":"<<master.legal_count<<",\"qualifying_pairs\":"<<total<<",\"distance_histogram\":\""<<hist_text(hist)<<"\",\"seconds\":"<<sec<<",\"reconstruction_verified\":true,\"coverage\":\""<<(records.size()==216&&total==expected.pair_count&&hist==cleaned?"EXACT COMPLETE":"PARTIAL")<<"\"}\n";write_atomic(out/"m19_recovery_stats.json",status.str());
    if(records.size()!=216||total!=expected.pair_count||hist!=cleaned)throw std::runtime_error("M19_D7_RECOVERY_COUNT_MISMATCH");
    std::cout<<"Recovered216 d7; full class histogram "<<hist_text(hist)<<" seconds="<<sec<<std::endl;
}

std::string blocker_cert(const Engine&e,const AllCuts&cuts,int gi,U s,int edge,int a){auto [u,v]=e.edges[edge];if(s>>edge&1)std::swap(u,v);std::ostringstream f;f<<"{\"M\":"<<M<<",\"graph_class\":"<<gi<<','<<graph_json(e)<<",\"orientation\":"<<s<<",\"blocked_edge\":"<<edge<<",\"tail\":"<<u<<",\"head\":"<<v<<",\"minimal_blocker\":"<<a<<",\"all_blockers\":"<<vector_json(cuts.blockers(s,edge))<<",\"cut_size\":"<<cuts.cut[a].total<<",\"coverage\":\"EXACT FOR LISTED GRAPH CLASSES\"}";return f.str();}
void block_graph(const Engine&e,int gi,std::ofstream&cert,std::ostream&csv){
    AllCuts cuts(e);std::array<uint64_t,21>hist{};uint64_t edges=0;
    for(U s=0;s<S;++s)if(e.legal[s]){
        std::array<int,20>intersection;intersection.fill(127);U blocked=0;
        std::array<int,127>outcounts{};
        for(int x=1;x<127;++x){U o=cuts.outgoing(s,x);int count=std::popcount(o);outcounts[x]=count;if(count==2){blocked|=o;while(o){int edge=std::countr_zero(o);o&=o-1;intersection[edge]&=x;}}}
        for(int id=0;id<M;++id){bool illegal=!e.legal[s^(1u<<id)];if(illegal!=bool(blocked>>id&1))throw std::runtime_error("INTERNAL_BLOCKER_INCONSISTENCY flip equivalence");
            if(!illegal)continue;int a=intersection[id];auto [u,v]=e.edges[id];if(s>>id&1)std::swap(u,v);
            if(a<=0||a>=127||!(a>>u&1)||(a>>v&1)||outcounts[a]!=2)throw std::runtime_error("INTERNAL_BLOCKER_INCONSISTENCY intersection");
            int c=cuts.cut[a].total;if(c<5)throw std::runtime_error("lambda violation");++hist[c];++edges;
            static int saved=0;if(c>=7&&saved<3){cert<<blocker_cert(e,cuts,gi,s,id,a)<<'\n';cert.flush();++saved;}
        }
    }
    uint64_t deep=0;int maximum=0;for(int i=5;i<=20;++i){if(hist[i])maximum=i;if(i>=7)deep+=hist[i];}
    csv<<M<<','<<gi<<','<<e.legal_count<<','<<edges<<','<<hist[5]<<','<<hist[6]<<','<<deep<<','<<maximum<<",\"";
    bool first=true;for(int i=5;i<=20;++i)if(hist[i]){if(!first)csv<<';';first=false;csv<<i<<':'<<hist[i];}csv<<"\",EXACT_COMPLETE_FOR_GRAPH\n";
    std::cout<<"Blockers M="<<M<<" class="<<gi<<" legal="<<e.legal_count<<" occurrences="<<edges<<" cut5="<<hist[5]<<" cut6="<<hist[6]<<" deep="<<deep<<" max="<<maximum<<std::endl;
}
void all_blockers(){
    init_tables();std::vector<std::pair<int,int>>list{{19,1888}};for(int i:hard20)list.emplace_back(20,i);
    fs::path csvpath=out/"all_state_blocker_size_per_graph.csv",cp=out/"all_state_blocker_checkpoint.txt";
    int next=0;std::string rows="M,graph_class,legal_states,blocked_edge_occurrences,cut5,cut6,cut7plus,maximum,histogram,coverage\n";
    if(fs::exists(cp)){std::ifstream f(cp);size_t bytes;f>>next>>bytes;if(next<0||next>39)throw std::runtime_error("blocker checkpoint");rows=read_all(csvpath);if(rows.size()<bytes)throw std::runtime_error("checkpoint CSV short");rows.resize(bytes);write_atomic(csvpath,rows);}
    std::ofstream cert(out/"blocker_size_7plus_certificates.jsonl",std::ios::app);Enumeration en;int current=0;
    for(int k=next;k<int(list.size());++k){auto [m,gi]=list[k];M=m;S=1u<<M;if(current!=M){en=enumerate_graphs();current=M;if(en.classes.size()!=size_t(M==19?8210:75701))throw std::runtime_error("graph checksum");}
        Engine e(en.classes.at(gi));e.prepare(workers());if(e.legal_count!=historical(M,gi).legal)throw std::runtime_error("CLASS_RECONSTRUCTION_MISMATCH");save_table(e,gi);
        std::ostringstream row;block_graph(e,gi,cert,row);rows+=row.str();write_atomic(csvpath,rows);write_atomic(cp,std::to_string(k+1)+" "+std::to_string(rows.size())+"\n");
        // Complete the current graph before taking the permitted early verdict.
        std::stringstream parse(row.str());std::string field;for(int i=0;i<7;++i)std::getline(parse,field,',');if(std::stoull(field)>0){std::cout<<"EARLY_BLOCKER_VERDICT after completed graph\n";break;}
    }
    cert.close();if(fs::file_size(out/"blocker_size_7plus_certificates.jsonl")==0)write_atomic(out/"blocker_size_7plus_certificates.jsonl","{\"record_type\":\"no_certificate\",\"reason\":\"No cut>=7 encountered in completed classes\"}\n");
}

void active_certificate(std::ofstream&f,const Engine&e,const AllCuts&cuts,int gi,int a,U internal,U sig,const std::vector<U>&states,const std::vector<U>&sizes,const std::vector<U>&reps,const std::vector<int>&ids,const std::vector<uint8_t>&label){
    f<<"{\"M\":"<<M<<",\"graph_class\":"<<gi<<','<<graph_json(e)<<",\"shore\":"<<a<<",\"internal_edge_mask\":"<<internal<<",\"internal_physical_edges\":[";for(size_t i=0;i<ids.size();++i){if(i)f<<',';int id=ids[i];f<<"{\"edge_id\":"<<id<<",\"endpoints\":["<<e.edges[id].u<<','<<e.edges[id].v<<"]}";}
    f<<"],\"outside_signature\":"<<sig<<",\"fiber_size\":"<<states.size()<<",\"component_sizes\":"<<vector_json(sizes)<<",\"representative_orientations\":"<<vector_json(reps)<<",\"component_boundary_states\":[";bool first=true;
    for(U s:states){std::vector<int>failed;for(int id:ids)if(!e.legal[s^(1u<<id)])failed.push_back(id);if(failed.empty())continue;
        if(!first)f<<',';first=false;f<<"{\"state\":"<<s<<",\"component\":"<<int(label[s])<<",\"legal_internal_flips\":[";bool firstmove=true;
        for(int id:ids){U t=s^(1u<<id);if(e.legal[t]){if(!firstmove)f<<',';firstmove=false;f<<"{\"edge\":"<<id<<",\"neighbor\":"<<t<<'}';}}
        f<<"],\"failed_internal_flips\":[";for(size_t i=0;i<failed.size();++i){if(i)f<<',';int id=failed[i];auto b=cuts.blockers(s,id);if(b.empty())throw std::runtime_error("internal blockers missing");f<<"{\"edge\":"<<id<<",\"blockers\":"<<vector_json(b)<<'}';}f<<"]}";
    }f<<"],\"coverage\":\"EXACT_COMPLETE_FOR_GRAPH\"}\n";f.flush();
}
void active(){
    init_tables();std::ofstream csv(out/"active_critical_fiber_results.csv"),cert(out/"active_critical_fiber_counterexamples.jsonl");
    csv<<"M,graph_class,legal_states,status,minimal_active_shore,internal_edges,fibers,nontrivial_fibers,max_fiber_size,connected_nontrivial_fibers,disconnected_nontrivial_fibers,coverage\n";
    uint64_t graphcount=0,noactive=0,shorecount=0,fibercount=0,ntcount=0,connected=0,disconnected=0;U maxfiber=0;
    for(int m:{19,20}){M=m;S=1u<<M;auto en=enumerate_graphs();if(en.classes.size()!=size_t(M==19?8210:75701))throw std::runtime_error("class checksum");std::vector<int>sel=M==19?std::vector<int>{1888}:hard20;
        for(int gi:sel){++graphcount;Engine e(en.classes.at(gi));auto p=out/("legal_M"+std::to_string(M)+"_class"+std::to_string(gi)+".bin");
            if(fs::exists(p))load_table(e,gi);else {e.prepare(workers());if(e.legal_count!=historical(M,gi).legal)throw std::runtime_error("legal mismatch");save_table(e,gi);}
            AllCuts cuts(e);auto sh=cuts.shores();std::map<int,U>internal;for(int a:sh){U mask=0;for(int id=0;id<M;++id)if((a>>e.edges[id].u&1)&&(a>>e.edges[id].v&1))mask|=1u<<id;if(mask)internal[a]=mask;}
            std::vector<int>minimal;for(auto [a,mask]:internal)if(std::none_of(internal.begin(),internal.end(),[&](auto v){int b=v.first;return a!=b&&(a&b)==b;}))minimal.push_back(a);
            if(minimal.empty()){++noactive;csv<<M<<','<<gi<<','<<e.legal_count<<",NO_ACTIVE_PROPER_CRITICAL_SHORE,,0,0,0,0,0,0,EXACT_COMPLETE_FOR_GRAPH\n";}
            for(int a:minimal){++shorecount;U mask=internal[a];std::vector<int>ids;for(int id=0;id<M;++id)if(mask>>id&1)ids.push_back(id);
                std::map<U,std::vector<U>>groups;for(U s=0;s<S;++s)if(e.legal[s])groups[s&~mask].push_back(s);
                std::vector<uint8_t>seen(S,0),label(S,0);std::vector<U>q;U largest=0;uint64_t nt=0,co=0,di=0;
                for(auto &[sig,states]:groups){largest=std::max(largest,U(states.size()));if(states.size()<2)continue;++nt;std::vector<U>sizes,reps;
                    for(U start:states)if(!seen[start]){q.clear();q.push_back(start);seen[start]=1;unsigned comp=sizes.size();if(comp>254)throw std::runtime_error("too many fiber components");label[start]=uint8_t(comp);reps.push_back(start);
                        for(size_t head=0;head<q.size();++head)for(int id:ids){U t=q[head]^(1u<<id);if(e.legal[t]&&!seen[t]){if((t&~mask)!=sig)throw std::runtime_error("outside signature changed");seen[t]=1;label[t]=uint8_t(comp);q.push_back(t);}}
                        sizes.push_back(U(q.size()));
                    }
                    if(std::accumulate(sizes.begin(),sizes.end(),uint64_t(0))!=states.size())throw std::runtime_error("fiber coverage");
                    if(sizes.size()>1){++di;active_certificate(cert,e,cuts,gi,a,mask,sig,states,sizes,reps,ids,label);}else ++co;
                }
                fibercount+=groups.size();ntcount+=nt;connected+=co;disconnected+=di;maxfiber=std::max(maxfiber,largest);
                csv<<M<<','<<gi<<','<<e.legal_count<<",TESTED,"<<a<<','<<ids.size()<<','<<groups.size()<<','<<nt<<','<<largest<<','<<co<<','<<di<<",EXACT_COMPLETE_FOR_GRAPH\n";csv.flush();
                std::cout<<"Active M="<<M<<" class="<<gi<<" shore="<<a<<" internal="<<ids.size()<<" fibers="<<groups.size()<<" nontrivial="<<nt<<" max="<<largest<<" disconnected="<<di<<std::endl;
            }
        }
    }
    if(!disconnected)cert<<"{\"record_type\":\"no_certificate\",\"reason\":\"All tested nontrivial fibers connected\",\"coverage\":\"EXACT FOR LISTED GRAPH CLASSES\"}\n";
    std::ostringstream f;f<<"{\"graphs_processed\":"<<graphcount<<",\"graphs_no_active\":"<<noactive<<",\"minimal_active_shores\":"<<shorecount<<",\"fibers\":"<<fibercount<<",\"nontrivial_fibers\":"<<ntcount<<",\"max_fiber_size\":"<<maxfiber<<",\"connected_nontrivial_fibers\":"<<connected<<",\"disconnected_nontrivial_fibers\":"<<disconnected<<"}\n";write_atomic(out/"active_fiber_stats.json",f.str());
    if(!shorecount)throw std::runtime_error("NO_ACTIVE_3A_3B: M18 fallback requires explicit handling");
}
}
int main(int argc,char**argv)try{
    if(argc!=2)throw std::runtime_error("mode recover|blockers|active required");second::out=fs::absolute(argv[0]).parent_path();std::string mode=argv[1];
    if(mode=="recover")second::recover();else if(mode=="blockers")second::all_blockers();else if(mode=="active")second::active();else throw std::runtime_error("unknown mode");return 0;
}catch(const std::exception&e){std::cerr<<"ERROR: "<<e.what()<<std::endl;return 1;}
