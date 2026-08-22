import heapq

INF=float("inf")

class RepeatedDijkstra:
    def __init__(self,n,undirected=False):
        self.n=n
        self.undirected=undirected
        self.adj=[[] for i in range(n) ]

    def add_edge(self,u,v,w):
        if w<0:
            raise ValueError("权值不得为负")
        else:
            self.adj[u].append((v,w))
            if self.undirected==True:
                self.adj[v].append((u,w))

    def dijkstra(self,source):
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
            for temp2 in self.adj[node]:
                if d+temp2[1]<dist[temp2[0]]:
                    dist[temp2[0]]=d+temp2[1]
                    parent[temp2[0]]=node
                    heapq.heappush(pq,(dist[temp2[0]],temp2[0]))

        return (dist,parent)

    def all_pairs(self):
        adj_List=[]
        for i in range(self.n):
            temp=self.dijkstra(i)[0]
            adj_List.append(temp)
        return adj_List

    def path(self,s,t):
        path=[t]
        temp=self.dijkstra(s)[1]
        current=temp[t]
        if current==-1:
            return []
        else:
            while current!=s:
                path.append(current)
                current=temp[current]
            path.append(s)
            path.reverse()
            return path
        
def test_repeated_dijkstra() -> None:
    # 情形 1：有向环状图，验证绕行更短
    # 0->1:1  1->2:2  2->3:3  3->0:4  0->2:10
    g = RepeatedDijkstra(4)
    for edge in [(0, 1, 1), (1, 2, 2), (2, 3, 3),
                 (3, 0, 4), (0, 2, 10)]:
        g.add_edge(*edge)

    d = g.all_pairs()
    # 期望：
    # 0 1 3 6
    # 9 0 2 5
    # 7 8 0 3
    # 4 5 7 0
    assert d == [[0, 1, 3, 6], [9, 0, 2, 5],
                 [7, 8, 0, 3], [4, 5, 7, 0]], d
    assert g.path(0, 3) == [0, 1, 2, 3], g.path(0, 3)

    # 情形 2：无向三角形，距离矩阵应对称
    u = RepeatedDijkstra(3, True)
    u.add_edge(0, 1, 1)
    u.add_edge(1, 2, 2)
    u.add_edge(0, 2, 4)
    du = u.all_pairs()
    # 0 1 3
    # 1 0 2
    # 3 2 0
    assert du[0][2] == du[2][0] == 3, du

    # 情形 3：不可达
    sp = RepeatedDijkstra(4)
    sp.add_edge(0, 1, 5)
    sp.add_edge(2, 3, 2)
    ds = sp.all_pairs()
    assert ds[0][2] == INF, ds
    assert ds[2][3] == 2, ds

    # 情形 4：单顶点
    one = RepeatedDijkstra(1)
    assert one.all_pairs()[0][0] == 0, one.all_pairs()

    # 情形 5：负权边应被拒绝
    try:
        g.add_edge(1, 0, -1)
        raise AssertionError("应当拒绝负权边")
    except ValueError as exc:
        print(exc)  # Dijkstra 不允许负权边

    print("所有测试通过")


if __name__ == "__main__":
    test_repeated_dijkstra()

            