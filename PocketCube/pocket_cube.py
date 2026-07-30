# 口袋魔方求解器 —— 问题 5-5 代码模板
# 第（f）问只需根据第（e）问中的算法，重写 solve(config) 函数
# 分隔线以下的代码无需修改

# ------------------------------------- #
# 根据第（e）问重写 solve               #
# ------------------------------------- #
def solve(config):
    # 返回复原 config 所需的一系列操作，若不可解则返回 None

    # ── 双向 BFS（第（e）问算法） ──
    parent1, frontier1 = {config: None}, [config]
    parent2, frontier2 = {SOLVED: None}, [SOLVED]
    flag = None
    count = 0
    while count < 7:
        frontier1 = explore_frontier(frontier1, parent1)
        frontier2 = explore_frontier(frontier2, parent2)
        overlap = parent1.keys() & parent2.keys()
        if overlap:
            flag = overlap.pop()
            break
        count += 1
    print('Searched %s reachable configurations' % (len(parent1) + len(parent2)))

    if flag is None:
        return None
    path1 = path_to_config(flag, parent1)
    path2 = path_to_config(flag, parent2)
    path2.reverse()
    return moves_from_path(path1 + path2[1:])

#   ── 原始代码（完整 BFS，访问约 300 万状态） ──
#   def solve(config):
#       parent, frontier = {config: None}, [config]
#       while len(frontier) != 0:
#           frontier = explore_frontier(frontier, parent, True)
#       print('Searched %s reachable configurations' % len(parent))
#
#       if SOLVED in parent:
#           path = path_to_config(SOLVED, parent)
#           return moves_from_path(path)
#       return None
# ------------------------------------- #
# 以下代码只需阅读，请勿修改             #
# ------------------------------------- #
# 口袋魔方的状态用长度为 24 的字符串表示
# 每个字符代表一个小立方体面的颜色
# 各面按拉丁十字展开图的阅读顺序排列

SOLVED = '001100223344112233554455'

def config_str(config):
    # 以拉丁十字展开图的形式返回状态的字符串表示
    return """
        %s%s
        %s%s
    %s%s%s%s%s%s%s%s
    %s%s%s%s%s%s%s%s
        %s%s
        %s%s
    """ % tuple(config)

def shift(A, d, ps):
    # 将列表 A 中位于索引 ps 处的值循环移动 d 个位置
    values = [A[p] for p in ps]
    k = len(ps)
    for i in range(k):
        A[ps[i]] = values[(i - d) % k]

def rotate(config, face, sgn):
    # 旋转给定状态的指定面，返回新状态
    # sgn == 1 时为顺时针旋转，sgn == -1 时为逆时针旋转
    assert face in (0, 1, 2)
    assert sgn in (-1, 1)
    if face is None:
        return config
    new_config = list(config)
    if face == 0:
        shift(new_config, 1 * sgn, [0, 1, 3, 2])
        shift(new_config, 2 * sgn, [11, 10, 9, 8, 7, 6, 5, 4])
    elif face == 1:
        shift(new_config, 1 * sgn, [4, 5, 13, 12])
        shift(new_config, 2 * sgn, [0, 2, 6, 14, 20, 22, 19, 11])
    elif face == 2:
        shift(new_config, 1 * sgn, [6, 7, 15, 14])
        shift(new_config, 2 * sgn, [2, 3, 8, 16, 21, 20, 13, 5])
    return ''.join(new_config)

def neighbors(config):
    # 返回 config 的所有邻居状态
    ns = []
    for face in (0, 1, 2):
        for sgn in (-1, 1):
            ns.append(rotate(config, face, sgn))
    return ns

def explore_frontier(frontier, parent, verbose=False):
    # 探索当前边界，将新状态加入 parent 和 new_frontier
    # 若 verbose 为 True，则打印当前边界的大小
    if verbose:
        print('Exploring next frontier containing # configs: %s' % len(frontier))
    new_frontier = []
    for f in frontier:
        for config in neighbors(f):
            if config not in parent:
                parent[config] = f
                new_frontier.append(config)
    return new_frontier

def path_to_config(config, parent):
    # 返回从 parent 树的根节点到 config 的状态路径
    path = [config]
    while path[-1] is not None:
        path.append(parent[path[-1]])
    path.pop()
    path.reverse()
    return path

def moves_from_path(path):
    # 给定状态路径，返回相邻状态之间的操作序列
    # 若路径上存在不相邻的状态对，则返回 None
    moves = []
    for i in range(1, len(path)):
        move = None
        for face in (0, 1, 2):
            for sgn in (-1, 1):
                if rotate(path[i - 1], face, sgn) == path[i]:
                    move = (face, sgn)
                    moves.append(move)
        if move is None:
            return None
    return moves

def path_from_moves(config, moves):
    # 从初始状态开始，依次执行给定操作，返回经过的状态路径
    path = [config]
    for move in moves:
        face, sgn = move
        config = rotate(config, face, sgn)
        path.append(config)
    return path

def scramble(config, n):
    # 对给定状态施加 n 次随机旋转，返回打乱后的新状态
    from random import randint
    for _ in range(n):
        ns = neighbors(config)
        i = randint(0, 2)
        config = ns[i]
    return config

def check(config, moves, verbose=False):
    # 检查从 config 出发执行 moves 是否能到达复原状态
    if verbose:
        print('Making %s moves from starting configuration:' % len(moves))
    path = path_from_moves(config, moves)
    if verbose:
        print(config_str(config))
    for i in range(1, len(path)):
        face, sgn = moves[i - 1]
        direction = 'clockwise'
        if sgn == -1:
            direction = 'counterclockwise'
        if verbose:
            print('Rotating face %s %s:' % (face, direction))
            print(config_str(path[i]))
    return path[-1] == SOLVED

def test(config):
    print('Solving configuration:')
    print(config_str(config))
    moves = solve(config)
    if moves is None:
        print('Path to solved state not found... :(')
        return
    print('Path to solved state found!')
    if check(config, moves):
        print('Move sequence terminated at solved state!')
    else:
        print('Move sequence did not terminate at solved state... :(')

if __name__ == '__main__':
    config = scramble(SOLVED, 100)
    test(config)
