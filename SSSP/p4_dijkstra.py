import heapq
from typing import List, Tuple


class DijkstraGraph:
    def __init__(self, n: int, undirected: bool = False):
        self.n = n
        self.undirected = undirected
        self.adj: List[List[Tuple[int, float]]] = [[] for _ in range(n)]

    def add_edge(self, u: int, v: int, weight: float) -> None:
        """
        添加边 u -> v，权值为 weight（必须 >= 0）。
        若 undirected=True，同时添加 v -> u。
        若 weight < 0，抛出 ValueError。
        """
        if weight<0:
            raise ValueError("权重不得为负值")
        self.adj[u].append((v,weight))

    def shortest_paths(self, source: int) -> Tuple[List[float], List[int]]:
        """
        使用最小堆 + 惰性删除运行 Dijkstra，
        返回 (dist, parent)。

        步骤提示：
        1. 初始化 dist 全为 inf，parent 全为 -1；dist[source]=0。
        2. 将 (0, source) 推入最小堆。
        3. 当堆非空时：
           - 弹出 (d, u)；
           - 若 d > dist[u]（惰性删除），跳过；
           - 遍历 u 的所有出边 (u, v, w)：
             若 dist[u] + w < dist[v]，更新 dist[v] 和 parent[v]，
             并将 (dist[v], v) 推入堆。
        4. 返回 dist, parent。
        """
        dist=[float("inf") for i in range(self.n)]
        dist[source]=0
        parent=[-1 for i in range(self.n)]
        parent[source]=source
        minHeap=[(0,source)]
        while minHeap:
            temp=heapq.heappop(minHeap)
            for i in self.adj[temp[1]]:
                if dist[i[0]]>dist[temp[1]]+i[1]:
                    dist[i[0]]=dist[temp[1]]+i[1]
                    parent[i[0]]=temp[1]
                    heapq.heappush(minHeap,(dist[i[0]],i[0]))
        return (dist,parent)

    @staticmethod
    def reconstruct_path(source: int, target: int, parent: List[int]) -> List[int]:
        """恢复 source 到 target 的最短路径。不可达则返回 []。"""
        path=[]
        current=target
        if parent[current]==-1:
            return path
        while current!=source:
            path.append(current)
            current=parent[current]
        path.append(source)
        path.reverse()
        return path


if __name__ == "__main__":
    # 情形 1：无向图，标准情形
    # 0 --4-- 1 --1-- 3 --3-- 4 --2-- 5
    # |       |     /         /
    # 1       2    5         7
    # |       |   /         /
    # 2 ------+  /         /
    #          1 ---------+
    g1 = DijkstraGraph(7, undirected=True)
    g1.add_edge(0, 1, 4)
    g1.add_edge(0, 2, 1)
    g1.add_edge(2, 1, 2)
    g1.add_edge(1, 3, 1)
    g1.add_edge(2, 3, 5)
    g1.add_edge(3, 4, 3)
    g1.add_edge(1, 4, 7)
    g1.add_edge(4, 5, 2)
    # 顶点 6 不可达

    dist, parent = g1.shortest_paths(0)
    print(dist)
    # [0, 3, 1, 4, 7, 9, inf]
    print(g1.reconstruct_path(0, 5, parent))
    # [0, 2, 1, 3, 4, 5]
    print(g1.reconstruct_path(0, 6, parent))
    # []

    # 情形 2：有向图，存在更短的绕路
    # 0 --(10)--> 1
    # 0 --(1)--> 2 --(1)--> 1
    g2 = DijkstraGraph(3)
    g2.add_edge(0, 1, 10)
    g2.add_edge(0, 2, 1)
    g2.add_edge(2, 1, 1)
    dist2, _ = g2.shortest_paths(0)
    print(dist2)  # [0, 2, 1]

    # 情形 3：非连通图，部分顶点不可达
    g3 = DijkstraGraph(4)
    g3.add_edge(0, 1, 5)
    g3.add_edge(2, 3, 2)  # 与 0 不连通
    dist3, _ = g3.shortest_paths(0)
    print(dist3)  # [0, 5, inf, inf]

    # 情形 4：单顶点
    g4 = DijkstraGraph(1)
    dist4, _ = g4.shortest_paths(0)
    print(dist4)  # [0]

    # 情形 5：稠密图，验证惰性删除正确性
    # 0 --(2)--> 1 --(2)--> 4
    # 0 --(1)--> 2 --(1)--> 3 --(1)--> 4
    # 0 --(5)--> 4
    g5 = DijkstraGraph(5)
    g5.add_edge(0, 1, 2)
    g5.add_edge(1, 4, 2)
    g5.add_edge(0, 2, 1)
    g5.add_edge(2, 3, 1)
    g5.add_edge(3, 4, 1)
    g5.add_edge(0, 4, 5)
    dist5, _ = g5.shortest_paths(0)
    print(dist5)
    # [0, 2, 1, 2, 3]  (0->2->3->4 = 3 < 0->1->4 = 4 < 0->4 = 5)

    # 情形 6：负权边应被拒绝
    try:
        g1.add_edge(0, 6, -1)
    except ValueError as error:
        print(error)  # Dijkstra 不允许负权边
