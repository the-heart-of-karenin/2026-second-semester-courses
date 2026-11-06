import unittest, random, itertools, json
from audit_core import *

class Regression(unittest.TestCase):
    @classmethod
    def setUpClass(cls):cls.cases=saved_pairs()
    def test_cut_counting_random(self):
        rng=random.Random(90230)
        for n in (3,4,5,6,7,8):
            for _ in range(20):
                edges=[tuple(rng.sample(range(n),2)) for _ in range(12)]
                g=Graph(edges,n);s=rng.randrange(1<<12)
                for x in g.cuts:
                    slow=sum(bool(x>>g.arc(s,e)[0]&1) and not bool(x>>g.arc(s,e)[1]&1) for e in range(12))
                    self.assertEqual(g.out(s,x),slow)
                    self.assertEqual(g.out(s,x)+g.out(s,g.full^x),g.cuts[x][2])
    def test_blockers_minimal_phase_saved(self):
        for c in self.cases:
            g=graph_of(c);s=c['source'];self.assertTrue(g.legal(s));self.assertTrue(g.legal(c['target']))
            g.skeleton()
            for e in range(g.M):
                b=g.family(s,e,2)
                self.assertEqual(not g.legal(s^(1<<e)),bool(b))
                if b:g.minimal(s,e)
                else:g.verify_flip(s,s^(1<<e),e)
            g.phases(s)
    def test_parallel_identity_and_all_states(self):
        # Two vertices, five distinct copies; all 32 physical states, twenty legal.
        g=Graph([(0,1)]*5,2);states=[s for s in range(32) if g.legal(s)]
        self.assertEqual(len(states),20)
        self.assertEqual(g.lam,5)
        s=3;t=5;self.assertEqual(s.bit_count(),t.bit_count());self.assertNotEqual(s,t)
        moves=[s^(1<<e) for e in range(5) if g.legal(s^(1<<e))]
        self.assertEqual(len(moves),3);self.assertEqual(len(set(moves)),3)
        for s in states:
            for e in range(5):
                self.assertEqual(not g.legal(s^(1<<e)),bool(g.family(s,e,2)))
                if not g.legal(s^(1<<e)):g.minimal(s,e)
                else:g.verify_flip(s,s^(1<<e),e)
    def test_path_fields_and_progress_semantics(self):
        for c in self.cases:
            g=graph_of(c)
            for p in c['paths']:
                nodes=p['nodes'];self.assertEqual(nodes[0]['state'],c['source'])
                for a,b in zip(nodes,nodes[1:]):
                    xor=a['state']^b['state'];self.assertEqual(xor.bit_count(),1);e=xor.bit_length()-1
                    self.assertEqual(b.get('flipped_edge',b.get('flipped_edge_from_previous')),e)
                    self.assertEqual(b.get('mismatch',b.get('mismatch_count')),(b['state']^c['target']).bit_count())
                    g.verify_flip(a['state'],b['state'],e)
                if p['kind']=='shortest_progress_path':
                    self.assertLessEqual((nodes[-1]['state']^c['target']).bit_count(),2)
                    self.assertTrue(all((a['state']^c['target']).bit_count()>2 for a in nodes[:-1]))
                if p['kind']=='shortest_source_target_path':self.assertEqual(nodes[-1]['state'],c['target'])
    def test_set_cover_exact(self):
        rng=random.Random(39)
        for _ in range(50):
            covers=[(i,rng.randrange(1,32)) for i in range(8)];full=0
            for _,b in covers:full|=b
            cover=exact_cover(covers,full)
            brute=min(len(c) for k in range(9) for c in itertools.combinations(covers,k) if functools.reduce(int.__or__,(b for _,b in c),0)==full)
            self.assertEqual(len(cover),brute)
    def test_restricted_fiber_connectivity(self):
        g=Graph([(0,1)]*5,2);states=[s for s in range(32) if g.legal(s)]
        fibers=fiber_components(states,3)
        self.assertEqual(sum(len(c) for cs in fibers.values() for c in cs),20)
        self.assertTrue(all(len(cs)==1 for cs in fibers.values()))
        for signature,cs in fibers.items():
            self.assertTrue(all(s & ~3==signature for c in cs for s in c))
        # Explicit allowed-state fixture: outside edge flips must not merge fibers;
        # changing two internal copies at once must not connect a component.
        split=fiber_components([0,3,4,7],3)
        self.assertEqual({sig:[len(c) for c in cs] for sig,cs in split.items()},{0:[1,1],4:[1,1]})

if __name__=='__main__':unittest.main(verbosity=2)
