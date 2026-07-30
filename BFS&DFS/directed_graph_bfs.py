from collections import defaultdict, deque
from typing import List


class DirectedGraphBFS:
    def __init__(self, n):
        """
        n: 顶点数量，顶点编号为 0 到 n-1
        """
        self.n = n
        self.adj = defaultdict(list)      # 有向邻接表
        self.indegree = [0] * n           # 每个顶点的入度

    def add_edge(self, u, v):
        """
        添加有向边 u -> v。
        注意：需要同时更新 indegree。
        """
        self.adj[u].append(v)
        self.indegree[v]+=1

    # def has_cycle(self):      # 原始版本 —— 每轮扫描全图 O(n²)
    #     indeg = self.indegree[:]
    #     queue = deque()
    #     finished = set()
    #     for i in range(self.n):
    #         if indeg[i] == 0:
    #             finished.add(i)
    #             queue.append(i)
    #             indeg[i] = -1
    #     while queue:
    #         for i in range(len(queue)):
    #             for j in self.adj[queue[i]]:
    #                 indeg[j] -= 1
    #         queue.popleft()
    #         for i in range(self.n):
    #             if indeg[i] == 0:
    #                 finished.add(i)
    #                 queue.append(i)
    #                 indeg[i] = -1
    #     return self.n != len(finished)

    def has_cycle(self):
        """
        使用 Kahn 算法（BFS）检测有向环：
        1. 将所有入度为 0 的顶点加入队列（仅初始扫描一次）。
        2. 逐一出队，将其邻居的入度减 1，
           若邻居入度降为 0 则立即入队。
        3. 统计处理的顶点总数，
           若等于 n 则无环，否则有环。
        复杂度：O(n + m)

        注意：has_cycle 可能被多次调用，
        每次调用时请使用 indegree 的副本，
        避免修改原始数据。
        """
        indeg=self.indegree[:]
        queue=deque()
        count=0
        for i in range(self.n):
            if indeg[i]==0:
                queue.append(i)
                count+=1
        while queue:
            node=queue.popleft()
            for i in self.adj[node]:
                indeg[i]-=1
                if indeg[i]==0:
                    queue.append(i)
                    count+=1
        return count!=self.n
        



if __name__ == "__main__":
    # 情形 1：有向无环图（与第 2 题情形 1 相同，结果应一致）
    bg1 = DirectedGraphBFS(4)
    bg1.add_edge(0, 1)
    bg1.add_edge(0, 2)
    bg1.add_edge(1, 3)
    bg1.add_edge(2, 3)
    print(bg1.has_cycle())  # False

    # 情形 2：含有向环
    bg2 = DirectedGraphBFS(3)
    bg2.add_edge(0, 1)
    bg2.add_edge(1, 2)
    bg2.add_edge(2, 0)
    print(bg2.has_cycle())  # True

    # 情形 3：自环
    bg3 = DirectedGraphBFS(2)
    bg3.add_edge(0, 1)
    bg3.add_edge(1, 1)
    print(bg3.has_cycle())  # True

    # 情形 4：多个连通分量，仅其中一个含环
    bg4 = DirectedGraphBFS(5)
    bg4.add_edge(0, 1)
    bg4.add_edge(1, 2)
    bg4.add_edge(3, 4)
    bg4.add_edge(4, 3)
    print(bg4.has_cycle())  # True

    # 情形 5：has_cycle 被多次调用，图结构不应改变
    bg5 = DirectedGraphBFS(3)
    bg5.add_edge(0, 1)
    bg5.add_edge(1, 2)
    print(bg5.has_cycle())  # False
    print(bg5.has_cycle())  # False（第二次调用结果应相同）
