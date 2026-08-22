from dataclasses import dataclass    #导入装饰器

@dataclass(frozen=True)              #自动生成样板的方法，frozen=True指的是不可变，可hash
class Edge:
    u:int
    v:int
    w:int

class Reweighting:
    def __init__(self,n):
        self.n=n
        self.edges=[]

    def add_edge(self,u,v,w):
        self.edges.append(Edge(u,v,w))

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

    def reweight(self,h):
        new_edges=[]
        for e in self.edges:
            new_edges.append(Edge(e.u,e.v,e.w+h[e.u]-h[e.v]))
        return new_edges

    def verify_non_negative(self,h):
        new_edges=self.reweight(self.compute_potentials())
        for e in new_edges:
            if e.w<0:
                return False
        return True

def test_reweighting() -> None:
    # 情形 1：CLRS 经典图，与第 1 题同一张图
    r = Reweighting(5)
    for edge in [
        (0, 1, 3), (0, 2, 8), (0, 4, -4),
        (1, 3, 1), (1, 4, 7), (2, 1, 4),
        (3, 0, 2), (3, 2, -5), (4, 3, 6),
    ]:
        r.add_edge(*edge)

    h = r.compute_potentials()
    assert h == [0, -1, -5, 0, -4], h
    assert r.verify_non_negative(h)
    print(*r.reweight(h), sep="\n")
    # 0->1:4   0->2:13  0->4:0
    # 1->3:0   1->4:10  2->1:0
    # 3->0:2   3->2:0   4->3:2

    # 情形 2：全部非负权，势函数应为全零
    pos = Reweighting(3)
    pos.add_edge(0, 1, 2)
    pos.add_edge(1, 2, 3)
    assert pos.compute_potentials() == [0, 0, 0]

    # 情形 3：负权环必须被检测到（即使它与其他顶点不连通）
    bad = Reweighting(4)
    bad.add_edge(0, 1, 1)
    bad.add_edge(2, 3, -2)
    bad.add_edge(3, 2, -2)      # 2 <-> 3 构成负权环
    try:
        bad.compute_potentials()
        raise AssertionError("应当检测到负权环")
    except ValueError as exc:
        print(exc)              # 图中存在负权环

    # 情形 4：非连通图，虚拟源点保证所有 h 都是有限值
    split = Reweighting(4)
    split.add_edge(0, 1, -3)
    split.add_edge(2, 3, -5)
    hs = split.compute_potentials()
    assert hs == [0, -3, 0, -5], hs
    assert split.verify_non_negative(hs)

    print("所有测试通过")


if __name__ == "__main__":
    test_reweighting()
