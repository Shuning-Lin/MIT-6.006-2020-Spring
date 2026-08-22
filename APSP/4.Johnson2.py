import heapq
from dataclasses import dataclass

INF=float("inf")

@dataclass(frozen=True)
class Edge:
    u:int
    v:int
    w:int

class Johnson:
    def __init__(self,n):
        self.n=n
        self.edges=[]

    def add_edge(self,u,v,w):
        self.edges.append(Edge(u,v,w))

    def all_pairs(self):
        d=[]
        t=[]
        h=self.compute_potentials()
        adj=self.reweight(h)
        for i in range(self.n):
            dist,trait=self.dijkstra(i,adj)
            for j in range(self.n):
                dist[j]=dist[j]-h[i]+h[j]
            d.append(dist)
            t.append(trait)
        return d

    def reweight(self,h):
        adj=[[] for i in range(self.n)]
        for e in self.edges:
            adj[e.u].append((e.v,e.w+h[e.u]-h[e.v]))
        return adj

    def compute_potentials(self):
        h=[0]*self.n
        for i in range(self.n-1):
            updated=False
            for e in self.edges:
                 if h[e.u]+e.w<h[e.v]:
                     h[e.v]=h[e.u]+e.w
                     updated=True
            if not updated:
                break
        for e in self.edges:
            if h[e.u]+e.w<h[e.v]:
                raise ValueError("存在负权环")
        return h

    def dijkstra(self,source,adj):
        dist=[INF]*self.n
        parent=[-1]*self.n
        dist[source]=0
        parent[source]=source

        pq=[]
        heapq.heappush(pq,(0,source))

        while pq:
            temp1=heapq.heappop(pq)
            node=temp1[1]
            d=temp1[0]
            if d>dist[node]:
                continue
            for temp2 in adj[node]:
                if d+temp2[1]<dist[temp2[0]]:
                    dist[temp2[0]]=d+temp2[1]
                    parent[temp2[0]]=node
                    heapq.heappush(pq,(dist[temp2[0]],temp2[0]))

        return dist,parent

    def path(self,s,t):
        h=self.compute_potentials()
        adj=self.reweight(h)
        dist,parent=self.dijkstra(s,adj)
        if dist[t]==INF:
            return []
        else:
            path=[]
            current=t
            while current!=s:
                path.append(current)
                current=parent[current]
            path.append(s)
            path.reverse()
            return path

    def path_weight(self, path):
        if not path:
            return INF
        wmap = {(e.u, e.v): e.w for e in self.edges} 
        return sum(wmap[(path[i], path[i+1])] for i in range(len(path)-1))

def test_johnson() -> None:
    # 情形 1：与第 1 题同一张图，结果必须与 Floyd-Warshall 完全一致
    j = Johnson(5)
    for edge in [
        (0, 1, 3), (0, 2, 8), (0, 4, -4),
        (1, 3, 1), (1, 4, 7), (2, 1, 4),
        (3, 0, 2), (3, 2, -5), (4, 3, 6),
    ]:
        j.add_edge(*edge)

    d = j.all_pairs()
    # 0   1  -3   2  -4
    # 3   0  -4   1  -1
    # 7   4   0   5   3
    # 2  -1  -5   0  -2
    # 8   5   1   6   0

    assert d == [[0, 1, -3, 2, -4], [3, 0, -4, 1, -1],
                 [7, 4, 0, 5, 3], [2, -1, -5, 0, -2],
                 [8, 5, 1, 6, 0]], d
    p = j.path(0, 2)
    assert p == [0, 4, 3, 2], p
    assert j.path_weight(p) == d[0][2] == -3

    # 情形 2：含不可达顶点，检验 INF 不参与减法
    iso = Johnson(6)
    iso.add_edge(0, 1, 3)
    iso.add_edge(1, 2, -5)
    # 顶点 3、4、5 孤立
    di = iso.all_pairs()
    assert di[0][2] == -2
    assert di[0][3] == INF and di[3][0] == INF
    assert di[5][5] == 0
    assert iso.path(0, 4) == []

    # 情形 3：负权环必须报错
    bad = Johnson(3)
    bad.add_edge(0, 1, 1)
    bad.add_edge(1, 2, -1)
    bad.add_edge(2, 1, -1)
    try:
        bad.all_pairs()
        raise AssertionError("应当检测到负权环")
    except ValueError as exc:
        print(exc)  # 图中存在负权环

    # 情形 4：单顶点与带自环
    one = Johnson(1)
    assert one.all_pairs()[0][0] == 0

    loop = Johnson(2)
    loop.add_edge(0, 1, 4)
    loop.add_edge(1, 1, 3)       # 正权自环，不影响结果
    assert loop.all_pairs()[0][1] == 4

    # 情形 5：与重复 Dijkstra 交叉验证（非负权图上两者应完全相同）
    jn = Johnson(4)
    for edge in [(0, 1, 1), (1, 2, 2), (2, 3, 3),
                 (3, 0, 4), (0, 2, 10)]:
        jn.add_edge(*edge)
    dj = jn.all_pairs()
    assert dj == [[0, 1, 3, 6], [9, 0, 2, 5],
                  [7, 8, 0, 3], [4, 5, 7, 0]], dj

    print("所有测试通过")


if __name__ == "__main__":
    test_johnson()


