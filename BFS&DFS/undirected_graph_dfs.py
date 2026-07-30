from typing import List, Set
from collections import defaultdict


class UndirectedGraph:
    def __init__(self, n):
        """
        n: 顶点数量，顶点编号为 0 到 n-1
        """
        self.n = n
        self.adj = defaultdict(list)  # 邻接表

    def add_edge(self, u, v):
        """添加无向边 (u, v)"""
        self.adj[u].append(v)
        self.adj[v].append(u)

    def _dfs_cycle(self, node, parent, visited):
        """
        DFS 辅助函数：
        - node:   当前正在访问的顶点
        - parent: 到达 node 时所来自的父顶点（-1 表示无父顶点）
        - visited: 已访问顶点的集合
        返回：若在以 node 为根的 DFS 子树中发现环则返回 True
        """
        visited.add(node)
        for i in self.adj[node]:
            if i == parent:
                continue

            if i in visited:
                return True

            if self._dfs_cycle(i, node, visited):
                return True
        return False

    def has_cycle(self):
        """
        外层函数：对所有未访问顶点逐一调用 _dfs_cycle，
        处理非连通图的情形。
        返回：图中是否存在环
        """
        flag=False
        visited:set[int]=set()
        for i in range(self.n):
            if i in visited:
                continue
            else:
                flag=flag or self._dfs_cycle(i,-1,visited)
        return flag

if __name__ == "__main__":
    # 情形 1：无环无向图（一棵树）
    # 0 - 1 - 2
    #     |
    #     3
    g1 = UndirectedGraph(4)
    g1.add_edge(0, 1)
    g1.add_edge(1, 2)
    g1.add_edge(1, 3)
    print(g1.has_cycle())  # False

    # 情形 2：含环无向图
    # 0 - 1 - 2
    #  \    /
    #   3
    #  即 0-1-2-3-0 构成一个环
    g2 = UndirectedGraph(4)
    g2.add_edge(0, 1)
    g2.add_edge(1, 2)
    g2.add_edge(2, 3)
    g2.add_edge(3, 0)
    print(g2.has_cycle())  # True

    # 情形 3：非连通图，仅其中一个连通分量含环
    # 分量 A：0 - 1 - 2（无环）
    # 分量 B：3 - 4 - 5 - 3（有环）
    g3 = UndirectedGraph(6)
    g3.add_edge(0, 1)
    g3.add_edge(1, 2)
    g3.add_edge(3, 4)
    g3.add_edge(4, 5)
    g3.add_edge(5, 3)
    print(g3.has_cycle())  # True

    # 情形 4：单顶点，无边
    g4 = UndirectedGraph(1)
    print(g4.has_cycle())  # False

    # 情形 5：两个顶点，一条边（不构成环）
    g5 = UndirectedGraph(2)
    g5.add_edge(0, 1)
    print(g5.has_cycle())  # False
