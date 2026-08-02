from collections import deque
from typing import List, Tuple


class UnweightedGraph:
    def __init__(self, n: int):
        self.n = n
        self.adj = [[] for _ in range(n)]

    def add_edge(self, u: int, v: int) -> None:
        """添加无向边 (u, v)。"""
        self.adj[u].append(v)
        self.adj[v].append(u)

    def shortest_paths(self, source: int) -> Tuple[List[float], List[int]]:
        """
        返回：
        dist[i]：source 到 i 的最少边数；
        parent[i]：最短路径中 i 的前驱。
        不可达顶点的距离为 inf，前驱为 -1。
        """
        dist=[float("inf") for i in range(self.n)]
        dist[source]=0
        parent=[-1 for i in range(self.n)]
        queue=deque([source])

        while queue:
            temp=queue.popleft()
            for i in self.adj[temp]:
                if dist[i]==float("inf"):
                    dist[i]=dist[temp]+1
                    parent[i]=temp
                    queue.append(i)
        return dist,parent
    @staticmethod
    def reconstruct_path(source: int, target: int, parent: List[int]) -> List[int]:
        """恢复 source 到 target 的路径，不可达则返回 []。"""
        path=[]
        current=target
        if parent[current]==-1 and current!=source:
            return path
        while current!=-1:
            path.append(current)
            current=parent[current]
        path.reverse()
        return path

            


if __name__ == "__main__":
    # 情形 1：简单连通图
    # 0 -- 1 -- 3 -- 4
    # |    |
    # 2 --+
    # 顶点 5 与其他顶点不连通
    g = UnweightedGraph(6)
    g.add_edge(0, 1)
    g.add_edge(0, 2)
    g.add_edge(1, 2)
    g.add_edge(1, 3)
    g.add_edge(3, 4)

    dist, parent = g.shortest_paths(0)

    print(dist)  # [0, 1, 1, 2, 3, inf]
    print(g.reconstruct_path(0, 4, parent))
    # 可能输出 [0, 1, 3, 4]

    print(g.reconstruct_path(0, 5, parent))
    # []

    # 情形 2：源点等于目标顶点
    dist2, parent2 = g.shortest_paths(1)
    print(dist2[1])           # 0
    print(g.reconstruct_path(1, 1, parent2))  # [1]

    # 情形 3：单顶点
    g3 = UnweightedGraph(1)
    dist3, _ = g3.shortest_paths(0)
    print(dist3)  # [0]
