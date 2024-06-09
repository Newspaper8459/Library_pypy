from array import array


class CSR:
  def __init__(self, n: int, edges: list[tuple[int, int]]) -> None:
    elist = array('i', [0]*len(edges))
    start = array('i', [0]*(n+1))

    for u, v in edges:
      start[u+1] += 1

    for i in range(n):
      start[i+1] += start[i]

    start_ = start[:]
    for u, v in edges:
      elist[start_[u]] = v
      start_[u] += 1

    self.elist = elist
    self.start = start



class SCCGraph:
  def __init__(self, n: int) -> None:
    """ACLのscc_graphです。面倒くさいので0-indexed実装です。add_edgeにぶち込む際は気を付けてください。

    Args:
        n (int): 頂点数
    """
    self.n = n
    self.edges: list[tuple[int, int]] = []

  def add_edge(self, u: int, v: int) -> None:
    """u -> v の有向辺を追加します。0-indexedです。

    Args:
        u (int): 始点
        v (int): 終点
    """

    assert 0 <= u < self.n and 0 <= v < self.n
    self.edges.append((u, v))

  def scc(self) -> list[list[int]]:
    """強連結成分分解された縮約グラフを返します。ACLのsccと同じ形式です。トポロジカルソートされていますが、同強連結成分内での頂点の順序、順位の等しい集合同士の順序は未定義です。

    Returns:
        list[list[int]]: sccされた縮約グラフ
    """

    csr = CSR(self.n, self.edges)
    elist = csr.elist
    start = csr.start
    now_ord = group_num = 0

    vis = array('i')

    order = array('i', [-1]*self.n)
    lowlink = array('i', [0]*self.n)
    ids = array('i', [0]*self.n)
    finished = array('h', [0]*self.n)
    parent = array('i', [-1]*self.n)

    for i in range(self.n):
      if order[i] != -1:
        continue

      q = array('i', [~i, i])
      while q:
        pos = q.pop()
        if pos >= 0:
          if finished[pos]:
            continue
          lowlink[pos] = order[pos] = now_ord
          now_ord += 1
          vis.append(pos)

          for j in range(start[pos], start[pos+1]):
            dest = elist[j]
            if order[dest] == -1:
              q.append(~dest)
              q.append(dest)
              parent[dest] = pos
            else:
              if order[dest] < lowlink[pos]:
                lowlink[pos] = order[dest]
        else:
          pos = ~pos
          if finished[pos]:
            continue
          finished[pos] = 1

          dest = parent[pos]
          if lowlink[dest] > lowlink[pos] and dest != -1:
            lowlink[dest] = lowlink[pos]

          if lowlink[pos] == order[pos]:
            while True:
              u = vis.pop()
              order[u] = 10**9
              ids[u] = group_num
              if u == pos:
                break
            group_num += 1

    for i in range(self.n):
      ids[i] = group_num - ids[i] - 1

    groups = [[] for _ in range(group_num)]
    for i in range(self.n):
      groups[ids[i]].append(i)

    return groups
