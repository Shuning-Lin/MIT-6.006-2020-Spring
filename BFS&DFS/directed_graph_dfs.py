from collections import defaultdict
from typing import List

WHITE, GRAY, BLACK = 0, 1, 2


class DirectedGraph:
    def __init__(self, n):
        """
        n: 顶点数量，顶点编号为 0 到 n-1
        """
        self.n = n
        self.adj = defaultdict(list)  # 有向邻接表

    def add_edge(self, u, v):
        """添加有向边 u -> v"""
        self.adj[u].append(v)

    def _dfs_cycle(self, node, color):
        """
        DFS 辅助函数（三色标记）：
        - node:  当前正在访问的顶点
        - color: 长度为 n 的列表，color[i] 为顶点 i 的当前颜色
        进入时将 node 标记为 GRAY；
        递归处理所有邻居；
        返回前将 node 标记为 BLACK。
        若发现邻居为 GRAY 则立即返回 True。
        """
        color[node]=1
        for i in self.adj[node]:
            if color[i]==0:
                 if self._dfs_cycle(i,color):
                     return True
            elif color[i]==1:
                return True
            else:
                continue
        color[node]=2
        return False
    def has_cycle(self):
        """
        外层函数：初始化 color 列表（全部设为 WHITE），
        遍历所有顶点，对每个 WHITE 顶点调用 _dfs_cycle。
        """
        flag=False
        color=[0]*self.n
        for i in range(self.n):
            if color[i]==0:
                flag=self._dfs_cycle(i,color) or flag
            elif color[i]==2:
                continue
            else:
                1#不会发生
        return flag


if __name__ == "__main__":
    # 情形 1：有向无环图（DAG）
    # 0 -> 1 -> 3
    # 0 -> 2 -> 3
    dg1 = DirectedGraph(4)
    dg1.add_edge(0, 1)
    dg1.add_edge(0, 2)
    dg1.add_edge(1, 3)
    dg1.add_edge(2, 3)
    print(dg1.has_cycle())  # False

    # 情形 2：含有向环
    # 0 -> 1 -> 2 -> 0
    dg2 = DirectedGraph(3)
    dg2.add_edge(0, 1)
    dg2.add_edge(1, 2)
    dg2.add_edge(2, 0)
    print(dg2.has_cycle())  # True

    # 情形 3：有向图，共享节点但无环
    # 0 -> 2
    # 1 -> 2
    # 验证：2 被访问两次，但不构成环
    dg3 = DirectedGraph(3)
    dg3.add_edge(0, 2)
    dg3.add_edge(1, 2)
    print(dg3.has_cycle())  # False

    # 情形 4：自环（顶点指向自身）
    dg4 = DirectedGraph(3)
    dg4.add_edge(0, 1)
    dg4.add_edge(1, 1)  # 自环
    print(dg4.has_cycle())  # True

    # 情形 5：多个连通分量，仅其中一个含环
    # 分量 A：0 -> 1 -> 2（无环）
    # 分量 B：3 -> 4 -> 3（有环）
    dg5 = DirectedGraph(5)
    dg5.add_edge(0, 1)
    dg5.add_edge(1, 2)
    dg5.add_edge(3, 4)
    dg5.add_edge(4, 3)
    print(dg5.has_cycle())  # True
