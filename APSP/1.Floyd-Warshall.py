INF=float("inf")

class FloydWarshall:
    def __init__(self,n):
        self.n=n
        self.dist=[[INF]*n for i in range(n)]
        self.nxt=[[-1]*n for i in range(n)]
        for i in range(n):
            self.dist[i][i]=0
            self.nxt[i][i]=i  #不太清楚这句话的作用

    def add_edge(self,u,v,w):
        if w<self.dist[u][v]:
            self.dist[u][v]=w
            self.nxt[u][v]=v

    def run(self):
        for k in range(self.n):
            for i in range(self.n):
                if self.dist[i][k] ==INF:
                    continue
                for j in range(self.n):
                    if self.dist[k][j]==INF:
                        continue
                    if self.dist[i][k]+self.dist[k][j]<self.dist[i][j]:
                        self.dist[i][j]=self.dist[i][k] +self.dist[k][j]
                        self.nxt[i][j]=self.nxt[i][k]

    def distance(self,i,j):
        return self.dist[i][j]

    def path(self,i,j):
        if self.nxt[i][j]==-1:
            return []
        if i==j:
            return [i]
        path=[i]
        current=self.nxt[i][j]
        step=0
        while current!=j and step<self.n:
            path.append(current)
            current=self.nxt[current][j]
            step+=1
        if current!=j:
            return []
        path.append(j)
        return path

    def has_negative_cycle(self):
        for i in range(self.n):
            if self.dist[i][i]<0:
                return True
        return False
def print_matrix(g: FloydWarshall, n: int) -> None:
    for i in range(n):
        print(*(g.distance(i, j) for j in range(n)))


def test_floyd_warshall() -> None:
    # 情形 1：CLRS 经典含负权边有向图，无负权环
    g = FloydWarshall(5)
    for u, v, w in [
        (0, 1, 3), (0, 2, 8), (0, 4, -4),
        (1, 3, 1), (1, 4, 7), (2, 1, 4),
        (3, 0, 2), (3, 2, -5), (4, 3, 6),
    ]:
        g.add_edge(u, v, w)
    g.run()

    print_matrix(g, 5)
    expected = [
        [0, 1, -3, 2, -4],
        [3, 0, -4, 1, -1],
        [7, 4, 0, 5, 3],
        [2, -1, -5, 0, -2],
        [8, 5, 1, 6, 0],
    ]
    for i in range(5):
        for j in range(5):
            assert g.distance(i, j) == expected[i][j], (i, j, g.distance(i, j))

    assert not g.has_negative_cycle()
    assert g.distance(0, 2) == -3
    assert g.path(0, 2) == [0, 4, 3, 2]

    # 情形 2：存在负权环（1 -> 2 -> 1，权值和 -2）
    neg = FloydWarshall(3)
    neg.add_edge(0, 1, 1)
    neg.add_edge(1, 2, -1)
    neg.add_edge(2, 1, -1)
    neg.run()
    assert neg.has_negative_cycle()
    assert neg.distance(1, 1) < 0

    # 情形 3：部分顶点不可达
    dis = FloydWarshall(4)
    dis.add_edge(0, 1, 5)
    dis.add_edge(2, 3, 2)          # 与 {0,1} 不连通
    dis.run()
    assert dis.distance(0, 1) == 5
    assert dis.distance(0, 2) == INF
    assert dis.path(0, 3) == []

    # 情形 4：单顶点
    one = FloydWarshall(1)
    one.run()
    assert one.distance(0, 0) == 0
    assert one.path(0, 0) == [0]

    # 情形 5：重边取最小
    multi = FloydWarshall(2)
    multi.add_edge(0, 1, 7)
    multi.add_edge(0, 1, 3)
    multi.run()
    assert multi.distance(0, 1) == 3

    print("所有测试通过")


if __name__ == "__main__":
    test_floyd_warshall()
