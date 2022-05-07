from collections import defaultdict
import graphviz

class DiGraph():
    def __init__(self):
        self.succ = defaultdict(dict)
        self.prec = defaultdict(dict)
        self.objects = dict()
        self.order = []
    
    def add(self, node1, node2, attribute={}):
        self.succ[node1].update({node2:attribute})
        self.prec[node2].update({node1:attribute})
        
    def map_object(self, node, obj):
        self.objects.update({node:obj})
        
    def add_object(self, obj):
        count = sum([obj.__class__ == o.__class__ for k, o in self.objects.items()])
        obj.name = f'{obj.__class__.__name__}_{count}'
        self.map_object(obj.name, obj)
        for obj_in in obj.inputs:
            self.add(obj_in.name, obj.name)
        self.order = self.topo_sort()
        
    @property
    def nodes(self):
        return set(self.prec.keys()).union(set(self.succ.keys()))
    
    def plot(self):
        gv = graphviz.Digraph()
        for node in self.succ:
            gv.node(node, label = f'{node}:{self.order.index(node)}')
            for succ in self.succ[node]:
                gv.edge(node, succ)
        return gv

    def topo_sort(self, l = None, visited = None):
        l = [] if l is None else l
        visited = {k:False for k in self.nodes} if visited is None else visited
        for u in self.nodes:
            if not visited[u]:
                self.dfs(u, l, visited)
        return l

    def dfs(self, u, l, visited):
        visited[u] = True
        for v in self.succ[u]:
            if not visited[v]:
                self.dfs(v, l, visited)
        l.insert(0, u)