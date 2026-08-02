from collections import deque
from typing import List, Tuple


class DAGShortestPath:
    def __init__(self, n: int):
        self.n = n
        self.adj: List[List[Tuple[int, float]]] = [[] for _ in range(n)]
        self.indegree: List[int] = [0] * n

    def add_edge(self, u: int, v: int, weight: float) -> None:
        """添加有向边 u -> v，权值为 weight，并更新入度。"""
        self.adj[u].append((v,weight))
        self.indegree[v]+=1

    def topological_sort(self) -> List[int]:
        """
        使用 Kahn 算法返回拓扑序。
        注意使用 indegree 的副本，避免改变图的原始数据。
        若图中存在有向环（处理的顶点数 < n），则抛出 ValueError。
        """
        topo=[]
        indeg=self.indegree[:]
        queue=deque([])
        for i in range(self.n):
            if indeg[i]==0:
                queue.append(i)
        while queue:
            node=queue.popleft()
            topo.append(node)
            for j in self.adj[node]:
                indeg[j[0]]-=1
                if indeg[j[0]]==0:
                    queue.append(j[0])
        if len(topo)!=self.n:
            raise ValueError("图中存在有向环")
        return topo

    def shortest_paths(self, source: int) -> Tuple[List[float], List[int]]:
        """
        先调用 topological_sort() 获取拓扑序，
        再按拓扑序松弛所有边，返回 (dist, parent)。

        步骤提示：
        1. 调用 topological_sort()（若含环则抛出 ValueError）。
        2. 初始化 dist 全为 inf，parent 全为 -1；dist[source]=0。
        3. 按拓扑序遍历每个顶点 u：
           - 若 dist[u] == inf，跳过（源点不可达）；
           - 遍历 u 的所有出边 (u, v, w)，执行松弛。
        """
        topo=self.topological_sort()

        dist=[float("inf") for i in range(self.n)]
        dist[source]=0
        parent=[-1 for i in range(self.n)]
        parent[source]=source

        for i in topo:
            if parent[i]==-1:
                continue
            else:
                for j in self.adj[i]:
                    if dist[j[0]]>dist[i]+j[1]:
                        parent[j[0]]=i
                        dist[j[0]]=dist[i]+j[1]

        return (dist,parent)


    @staticmethod
    def reconstruct_path(source: int, target: int, parent: List[int]) -> List[int]:
        """恢复 source 到 target 的最短路径。不可达则返回 []。"""
        path=[]
        if parent==-1:
            return path
        current=target
        while current!=source:
            path.append(current)
            current=parent[current]
        path.append(source)
        path.reverse()
        return path
            


if __name__ == "__main__":
    # 情形 1：标准 DAG 含负权边
    dag = DAGShortestPath(7)
    dag.add_edge(0, 1, 5)
    dag.add_edge(0, 2, 3)
    dag.add_edge(1, 3, 6)
    dag.add_edge(1, 2, 2)
    dag.add_edge(2, 4, 4)
    dag.add_edge(2, 5, 2)
    dag.add_edge(2, 3, 7)
    dag.add_edge(3, 4, -1)
    dag.add_edge(4, 5, -2)
    # 顶点 6 不可达

    dist, parent = dag.shortest_paths(0)
    print(dist)
    # [0, 5, 3, 10, 7, 5, inf]

    print(dag.reconstruct_path(0, 5, parent))
    # [0, 2, 5]，距离为 5

    # 情形 2：含环图不能使用 DAG Relaxation
    cyclic = DAGShortestPath(3)
    cyclic.add_edge(0, 1, 1)
    cyclic.add_edge(1, 2, 1)
    cyclic.add_edge(2, 0, 1)

    try:
        cyclic.shortest_paths(0)
    except ValueError as error:
        print(error)  # 图中存在有向环

    # 情形 3：源点为中间节点
    dag3 = DAGShortestPath(4)
    dag3.add_edge(0, 1, 1)
    dag3.add_edge(1, 2, 1)
    dag3.add_edge(2, 3, 1)
    dist3, _ = dag3.shortest_paths(1)
    print(dist3)  # [inf, 0, 1, 2]

    # 情形 4：单顶点
    single = DAGShortestPath(1)
    dist_s, _ = single.shortest_paths(0)
    print(dist_s)  # [0]
