// Shared verified generator, Engine and AllCuts; old stage entry points never called.
#include "third_stage_shared.inc"
using namespace second;

std::vector<std::string> fields(const std::string &s){std::vector<std::string>r;std::string a;bool quote=false;for(char c:s){if(c=='"')quote=!quote;else if(c==','&&!quote){r.push_back(a);a.clear();}else a+=c;}r.push_back(a);return r;}
void verify_graph(const Engine&e,int gi){std::ifstream f(out/"third_graph_multiplicities.txt");int m,id;while(f>>m>>id){Graph g{};int v;for(auto&x:g){if(!(f>>v))throw std::runtime_error("graph fixture format");x=uint8_t(v);}if(m==M&&id==gi){if(g!=e.graph)throw std::runtime_error("CLASS_RECONSTRUCTION_MISMATCH multiplicities");return;}}throw std::runtime_error("class fixture not found");}
std::string record_certificate(const Engine&e,const AllCuts&cuts,int gi,U s,int edge,int a,int previous){auto base=blocker_cert(e,cuts,gi,s,edge,a);base.pop_back();std::vector<U>verts;for(int v=0;v<7;++v)if(a>>v&1)verts.push_back(v);return base+",\"minimal_blocker_vertex_set\":"+vector_json(verts)+",\"out_cut\":"+std::to_string(std::popcount(cuts.outgoing(s,a)))+",\"in_cut\":"+std::to_string(cuts.cut[a].total-2)+",\"previous_maximum\":"+std::to_string(previous)+",\"origin\":\"NEW_GLOBAL_RECORD\"}";}

void depth(){
    M=20;S=1u<<M;init_tables();auto en=enumerate_graphs();if(en.classes.size()!=75701)throw std::runtime_error("class checksum");
    fs::path csvpath=out/"m20_hard38_blocker_depth_per_graph.csv",cp=out/"m20_blocker_depth_checkpoint.txt";
    std::string rows="M,graph_class,legal_states,blocked_edge_occurrences,cut5,cut6,cut7plus,maximum,histogram,source\n";
    int next=2,globalmax=7;
    if(fs::exists(cp)){size_t bytes;std::ifstream f(cp);f>>next>>globalmax>>bytes;if(next<2||next>38)throw std::runtime_error("depth checkpoint index");rows=read_all(csvpath);if(rows.size()<bytes)throw std::runtime_error("depth checkpoint short");rows.resize(bytes);write_atomic(csvpath,rows);}
    else {rows+=read_all(out/"m20_depth_seed.txt");write_atomic(csvpath,rows);write_atomic(cp,"2 7 "+std::to_string(rows.size())+"\n");}
    std::ofstream cert(out/"blocker_depth_record_certificates.jsonl",std::ios::app);
    for(int k=next;k<38;++k){int gi=hard20[k];Engine e(en.classes.at(gi));verify_graph(e,gi);load_table(e,gi);AllCuts cuts(e);std::array<uint64_t,21>hist{};uint64_t edgecount=0;
        for(U s=0;s<S;++s)if(e.legal[s]){std::array<int,20>intersection;intersection.fill(127);std::array<int,127>counts{};U blocked=0;
            for(int x=1;x<127;++x){U o=cuts.outgoing(s,x);counts[x]=std::popcount(o);if(counts[x]==2){blocked|=o;while(o){int id=std::countr_zero(o);o&=o-1;intersection[id]&=x;}}}
            for(int id=0;id<M;++id){bool illegal=!e.legal[s^(1u<<id)];if(illegal!=bool(blocked>>id&1))throw std::runtime_error("INTERNAL_BLOCKER_INCONSISTENCY flip equivalence");if(!illegal)continue;
                int a=intersection[id];auto [u,v]=e.edges[id];if(s>>id&1)std::swap(u,v);if(a<=0||a>=127||!(a>>u&1)||(a>>v&1)||counts[a]!=2)throw std::runtime_error("INTERNAL_BLOCKER_INCONSISTENCY minimal");
                int c=cuts.cut[a].total;++hist[c];++edgecount;if(c>globalmax){cert<<record_certificate(e,cuts,gi,s,id,a,globalmax)<<'\n';cert.flush();globalmax=c;}
            }
        }
        uint64_t deep=0;int maximum=0;std::ostringstream h;bool first=true;for(int i=5;i<=20;++i)if(hist[i]){maximum=i;if(i>=7)deep+=hist[i];if(!first)h<<';';first=false;h<<i<<':'<<hist[i];}
        std::ostringstream r;r<<M<<','<<gi<<','<<e.legal_count<<','<<edgecount<<','<<hist[5]<<','<<hist[6]<<','<<deep<<','<<maximum<<",\""<<h.str()<<"\",NEW_BLOCKER_DEPTH_TEST\n";rows+=r.str();write_atomic(csvpath,rows);write_atomic(cp,std::to_string(k+1)+" "+std::to_string(globalmax)+" "+std::to_string(rows.size())+"\n");
        std::cout<<"Depth "<<k+1<<"/38 class="<<gi<<" histogram="<<h.str()<<" globalmax="<<globalmax<<std::endl;
    }
}

struct FiberTotals{uint64_t fibers=0,nt=0,maximum=0,connected=0,disconnected=0;};
struct Reuse{int internal_count;FiberTotals total;};
void full_certificate(std::ofstream&f,const Engine&e,const AllCuts&cuts,int gi,int a,U mask,U sig,const std::vector<int>&ids,const std::vector<U>&states,const std::vector<U>&sizes,const std::vector<U>&reps,const std::vector<U>&label){
    f<<"{\"M\":"<<M<<",\"graph_class\":"<<gi<<','<<graph_json(e)<<",\"shore\":"<<a<<",\"shore_size\":"<<std::popcount(unsigned(a))<<",\"internal_edge_ids\":[";for(size_t i=0;i<ids.size();++i){if(i)f<<',';f<<ids[i];}f<<"],\"internal_edge_mask\":"<<mask<<",\"outside_signature\":"<<sig<<",\"fiber_size\":"<<states.size()<<",\"component_sizes\":"<<vector_json(sizes)<<",\"representative_orientations\":"<<vector_json(reps)<<",\"states\":[";
    for(size_t i=0;i<states.size();++i){U s=states[i];if(i)f<<',';f<<"{\"orientation\":"<<s<<",\"component\":"<<label[s]<<",\"legal_internal_neighbors\":[";bool first=true;
        for(int id:ids){U t=s^(1u<<id);if(e.legal[t]){if(!first)f<<',';first=false;f<<"{\"edge\":"<<id<<",\"state\":"<<t<<'}';}}
        f<<"],\"failed_internal_flips\":[";first=true;for(int id:ids)if(!e.legal[s^(1u<<id)]){if(!first)f<<',';first=false;auto b=cuts.blockers(s,id);if(b.empty())throw std::runtime_error("missing internal blocker");f<<"{\"edge\":"<<id<<",\"tight_blockers\":"<<vector_json(b)<<'}';}f<<"]}";
    }f<<"],\"coverage\":\"EXACT_COMPLETE_FOR_GRAPH\"}\n";f.flush();
}
void fibers(){
    init_tables();std::map<std::tuple<int,int,int>,Reuse>reuse;std::ifstream input(out/"minimal_active_reuse.txt");int m,gi,a,n;FiberTotals t;
    while(input>>m>>gi>>a>>n>>t.fibers>>t.nt>>t.maximum>>t.connected>>t.disconnected)reuse[{m,gi,a}]={n,t};if(reuse.size()!=64)throw std::runtime_error("minimal active reuse count");
    std::ofstream shorescsv(out/"all_active_critical_shores.csv"),results(out/"all_active_fiber_results.csv"),cert(out/"all_active_fiber_counterexamples.jsonl");
    shorescsv<<"M,graph_class,shore,shore_size,active,minimal_active,parent_shore,tree_depth,active_descendants,active_ancestors,internal_edges\n";
    results<<"M,graph_class,shore,shore_size,internal_edges,tree_depth,active_descendants,active_ancestors,fibers,nontrivial_fibers,max_fiber_size,connected_nontrivial_fibers,disconnected_nontrivial_fibers,source,coverage\n";
    size_t reused=0;uint64_t disconnected=0;
    for(int m:{19,20}){M=m;S=1u<<M;auto en=enumerate_graphs();if(en.classes.size()!=size_t(M==19?8210:75701))throw std::runtime_error("graph checksum");std::vector<int>sel=M==19?std::vector<int>{1888}:hard20;
        for(int gi:sel){Engine e(en.classes.at(gi));verify_graph(e,gi);load_table(e,gi);AllCuts cuts(e);auto sh=cuts.shores();std::map<int,U>masks;std::map<int,int>parent,level;
            for(int a:sh){U mask=0;for(int id=0;id<M;++id)if((a>>e.edges[id].u&1)&&(a>>e.edges[id].v&1))mask|=1u<<id;masks[a]=mask;int p=127;for(int b:sh)if(a!=b&&(a&b)==a&&std::popcount(unsigned(b))<std::popcount(unsigned(p)))p=b;parent[a]=p;}
            for(int a:sh){int p=a,d=0;while(p!=127){++d;p=parent.at(p);}level[a]=d;}
            for(int a:sh){U mask=masks[a];bool active=mask!=0;int desc=0,anc=0;for(int b:sh)if(a!=b&&masks[b]){desc+=(a&b)==b;anc+=(a&b)==a;}bool minimal=active&&desc==0;
                shorescsv<<M<<','<<gi<<','<<a<<','<<std::popcount(unsigned(a))<<','<<active<<','<<minimal<<','<<parent[a]<<','<<level[a]<<','<<desc<<','<<anc<<','<<std::popcount(mask)<<'\n';
                if(!active)continue;FiberTotals total;std::string source;std::vector<int>ids;for(int id=0;id<M;++id)if(mask>>id&1)ids.push_back(id);
                auto old=reuse.find({M,gi,a});if(old!=reuse.end()){if(!minimal||old->second.internal_count!=int(ids.size()))throw std::runtime_error("reused shore mismatch");total=old->second.total;source="REUSED_MINIMAL_ACTIVE_RESULT";++reused;}
                else {if(minimal)throw std::runtime_error("missing minimal-active saved result");source="NEW_ALL_ACTIVE_TEST";
                    std::map<U,std::vector<U>>groups;for(U s=0;s<S;++s)if(e.legal[s])groups[s&~mask].push_back(s);total.fibers=groups.size();std::vector<uint8_t>seen(S,0);std::vector<U>q,label(S,0);
                    for(auto &[sig,states]:groups){total.maximum=std::max(total.maximum,uint64_t(states.size()));if(states.size()==1)continue;++total.nt;std::vector<U>sizes,reps;
                        for(U start:states)if(!seen[start]){q.clear();q.push_back(start);seen[start]=1;U comp=U(sizes.size());label[start]=comp;reps.push_back(start);
                            for(size_t head=0;head<q.size();++head)for(int id:ids){U t=q[head]^(1u<<id);if(e.legal[t]&&!seen[t]){if((t&~mask)!=sig)throw std::runtime_error("outside signature changed");seen[t]=1;label[t]=comp;q.push_back(t);}}
                            sizes.push_back(U(q.size()));
                        }
                        if(std::accumulate(sizes.begin(),sizes.end(),uint64_t(0))!=states.size())throw std::runtime_error("fiber coverage mismatch");
                        if(sizes.size()>1){++total.disconnected;full_certificate(cert,e,cuts,gi,a,mask,sig,ids,states,sizes,reps,label);}else ++total.connected;
                    }
                }
                disconnected+=total.disconnected;
                results<<M<<','<<gi<<','<<a<<','<<std::popcount(unsigned(a))<<','<<ids.size()<<','<<level[a]<<','<<desc<<','<<anc<<','<<total.fibers<<','<<total.nt<<','<<total.maximum<<','<<total.connected<<','<<total.disconnected<<','<<source<<",EXACT_COMPLETE_FOR_GRAPH\n";results.flush();
                std::cout<<"All-active M="<<M<<" class="<<gi<<" A="<<a<<" depth="<<level[a]<<" internal="<<ids.size()<<" fibers="<<total.fibers<<" max="<<total.maximum<<" disconnected="<<total.disconnected<<' '<<source<<std::endl;
            }
        }
    }
    if(reused!=64)throw std::runtime_error("not all64 minimal active results reused");if(!disconnected)cert<<"{\"record_type\":\"no_certificate\",\"reason\":\"No disconnected all-active fiber in exact39-graph universe\"}\n";
}
int main(int argc,char**argv)try {if(argc!=2)throw std::runtime_error("mode depth|fibers");out=fs::absolute(argv[0]).parent_path();std::string mode=argv[1];if(mode=="depth")depth();else if(mode=="fibers")fibers();else throw std::runtime_error("bad mode");return 0;}catch(const std::exception&e){std::cerr<<"ERROR: "<<e.what()<<std::endl;return 1;}
