from typing import List, Tuple

class BellmanFordGraph:
    def __init__(self, n: int):
        self.n = n
        self.edges: List[Tuple[int, int, float]] = []

    def add_edge(self, u: int, v: int, weight: float) -> None:
        """添加有向边 u -> v，权值为 weight。"""
        self.edges.append((u,v,weight))

    def shortest_paths(self, source: int) -> Tuple[List[float], List[int]]:
        """
        返回源点到各顶点的最短距离和前驱数组。

        步骤提示：
        1. 初始化 dist 全为 inf，parent 全为 -1；dist[source]=0。
        2. 进行 n-1 轮松弛，每轮用 updated 标记实现提前终止。
        3. 第 n 轮检测负权环：若仍可松弛且 dist[u]!=inf，
           抛出 ValueError("存在从源点可达的负权环")。
        """
        dist=[float("inf") for i in range(self.n)]
        dist[source]=0
        parent=[-1 for i in range(self.n)]
        parent[source]=source

        for i in range(self.n-1):
            flag=True
            for j in self.edges:
                if  dist[j[0]]!=float("inf"):
                    if dist[j[0]]+j[2]<dist[j[1]]:
                        parent[j[1]]=j[0]
                        dist[j[1]]=dist[j[0]]+j[2]
                        flag=False
            if flag:
                break
        #判断
        flag=False
        for j in self.edges:
            if  dist[j[0]]!=float("inf"):
                if dist[j[0]]+j[2]<dist[j[1]]:
                    parent[j[1]]=j[0]
                    dist[j[1]]=dist[j[0]]+j[2]
                    flag=True
        if flag:
            raise ValueError("存在从原点可达的负权环")
        return (dist,parent)
        


    @staticmethod
    def reconstruct_path(
        source: int, target: int, parent: List[int]
    ) -> List[int]:
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
    # 情形 1：含负权边，但不存在负权环
    graph = BellmanFordGraph(6)
    graph.add_edge(0, 1, 6)
    graph.add_edge(0, 2, 7)
    graph.add_edge(1, 2, 8)
    graph.add_edge(1, 3, 5)
    graph.add_edge(1, 4, -4)
    graph.add_edge(2, 3, -3)
    graph.add_edge(2, 4, 9)
    graph.add_edge(3, 1, -2)
    graph.add_edge(4, 0, 2)
    graph.add_edge(4, 3, 7)

    dist, parent = graph.shortest_paths(0)
    print(dist)  # [0, 2, 7, 4, -2, inf]
    print(graph.reconstruct_path(0, 4, parent))
    # [0, 2, 3, 1, 4]

    # 情形 2：存在从源点可达的负权环
    # 0 --(1)--> 1 --(-2)--> 2 --(-2)--> 1  (1<->2 负权环)
    negative_cycle = BellmanFordGraph(4)
    negative_cycle.add_edge(0, 1, 1)
    negative_cycle.add_edge(1, 2, -2)
    negative_cycle.add_edge(2, 1, -2)
    negative_cycle.add_edge(2, 3, 1)

    try:
        negative_cycle.shortest_paths(0)
    except ValueError as error:
        print(error)  # 存在从源点可达的负权环

    # 情形 3：负权环不可达，不影响从源点 0 出发的结果
    # 分量 A：0 --(3)--> 1 --(4)--> 2（无环）
    # 分量 B：3 --(-1)--> 4 --(-1)--> 3（负权环，但从 0 不可达）
    unreachable_cycle = BellmanFordGraph(5)
    unreachable_cycle.add_edge(0, 1, 3)
    unreachable_cycle.add_edge(1, 2, 4)
    unreachable_cycle.add_edge(3, 4, -1)
    unreachable_cycle.add_edge(4, 3, -1)

    dist, _ = unreachable_cycle.shortest_paths(0)
    print(dist)  # [0, 3, 7, inf, inf]

    # 情形 4：含负权边，提前终止验证
    bf4 = BellmanFordGraph(3)
    bf4.add_edge(0, 1, 2)
    bf4.add_edge(0, 2, 4)
    dist4, _ = bf4.shortest_paths(0)
    print(dist4)  # [0, 2, 4]

    # 情形 5：单顶点
    bf5 = BellmanFordGraph(1)
    dist5, _ = bf5.shortest_paths(0)
    print(dist5)  # [0]
