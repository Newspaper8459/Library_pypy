from __future__ import annotations
from typing import Final, SupportsIndex, overload


_misaizu_lib_mod: Final[int] = 998244353
# _misaizu_lib_mod: Final[int] = 1000000007

class Matrix:
  @staticmethod
  def zeros(n: int, m: int, mod: bool = False):
    a = [[0]*m for _ in range(n)]
    return Matrix(a, mod)

  @staticmethod
  def ones(n: int, m: int, mod: bool = False):
    a = [[1]*m for _ in range(n)]
    return Matrix(a, mod)

  @staticmethod
  def identity(n: int, mod: bool = False):
    a = [[int(i==j) for j in range(n)] for i in range(n)]
    return Matrix(a, mod)

  @overload
  def __init__(self, a: list[int], mod: bool) -> None: ...
  @overload
  def __init__(self, a: list[int], n: int, m: int, mod: bool) -> None: ...
  @overload
  def __init__(self, a: list[list[int]], mod: bool) -> None: ...

  def __init__(self, a, n=-1, m=-1, mod=True):
    if not isinstance(a, list):
      raise TypeError

    self._mod = mod

    if isinstance(a[0], int):
      if n == m == -1:
        self.n = -1
        self.m = len(a)
        if mod:
          a = [i%_misaizu_lib_mod for i in a]
        self.a = [a]
      elif n != -1 and m != -1:
        assert n*m == len(a)

        self.n = n
        self.m = m
        if mod:
          a = [i%_misaizu_lib_mod for i in a]
        a = [[a[i*m+j] for j in range(m)] for i in range(n)]
        self.a = a
      else:
        raise AssertionError()
    elif isinstance(a[0], list) and isinstance(a[0][0], int):
      self.n = len(a)
      self.m = len(a[0])
      if mod:
        a = [[j%_misaizu_lib_mod for j in i] for i in a]
      self.a = a
    else:
      raise TypeError()

  def __str__(self) -> str:
    return self.a.__str__()

  def __repr__(self) -> str:
    return self.a.__repr__()

  def __len__(self):
    return self.n

  @overload
  def __getitem__(self, __i: SupportsIndex) -> list[int]: ...
  @overload
  def __getitem__(self, __s: slice) -> list[list[int]]: ...

  def __getitem__(self, __key):
    return self.a.__getitem__(__key)

  @overload
  def __setitem__(self, __i: SupportsIndex, __value: list[int]): ...
  @overload
  def __setitem__(self, __s: slice, __value: list[list[int]]): ...

  def __setitem__(self, __key, __value):
    return self.a.__setitem__(__key, __value)

  def __add__(self, __mat: Matrix) -> Matrix:
    if not isinstance(__mat, Matrix):
      raise TypeError()

    assert(self.n == __mat.n and self.m == __mat.m), f""

    C = [[0]*self.m for _ in range(self.n)]
    for i in range(self.n):
      a = self.a[i]
      b = __mat.a[i]
      c = C[i]
      for j in range(self.m):
        c[j] = a[j] + b[j]
        if self._mod or __mat._mod:
          c[j] %= _misaizu_lib_mod
    return Matrix(C, self._mod|__mat._mod)

  def __iadd__(self, __mat: Matrix) -> Matrix:
    if not isinstance(__mat, Matrix):
      raise TypeError()

    assert(self.n == __mat.n and self.m == __mat.m), f""

    for i in range(self.n):
      a = self.a[i]
      b = __mat.a[i]
      for j in range(self.m):
        a[j] += b[j]
        if self._mod or __mat._mod:
          a[j] %= _misaizu_lib_mod
    return self

  def __sub__(self, __mat: Matrix) -> Matrix:
    if not isinstance(__mat, Matrix):
      raise TypeError()

    assert(self.n == __mat.n and self.m == __mat.m), f""

    C = [[0]*self.m for _ in range(self.n)]
    for i in range(self.n):
      a = self.a[i]
      b = __mat.a[i]
      c = C[i]
      for j in range(self.m):
        c[j] = a[j] - b[j]
        if self._mod or __mat._mod:
          c[j] %= _misaizu_lib_mod
    return Matrix(C, self._mod|__mat._mod)

  def __isub__(self, __mat: Matrix) -> Matrix:
    if not isinstance(__mat, Matrix):
      raise TypeError()

    assert(self.n == __mat.n and self.m == __mat.m), f""

    for i in range(self.n):
      a = self.a[i]
      b = __mat.a[i]
      for j in range(self.m):
        a[j] -= b[j]
        if self._mod or __mat._mod:
          a[j] %= _misaizu_lib_mod
    return self

  def __matmul__(self, __mat: Matrix) -> Matrix:
    if not isinstance(__mat, Matrix):
      raise TypeError()

    assert self.m == __mat.n, f""

    I, J, K = self.n, __mat.m, __mat.n
    C = [[0]*J for _ in range(I)]
    for i in range(I):
      a = self.a[i]
      c = C[i]
      for k in range(K):
        b = __mat.a[k]
        for j in range(J):
          c[j] += a[k]*b[j]
          if self._mod or __mat._mod:
            c[j] %= _misaizu_lib_mod
    return Matrix(C, self._mod|__mat._mod)

  def __imatmul__(self, __mat: Matrix) -> Matrix:
    return self.__matmul__(__mat)

  def __mul__(self, __value: Matrix|int) -> Matrix:
    if isinstance(__value, int):
      C = [[0]*self.m for _ in range(self.n)]
      for i in range(self.n):
        a = self.a[i]
        c = C[i]
        for j in range(self.m):
          c[j] = a[j] * __value
          if self._mod:
            c[j] %= _misaizu_lib_mod
      return Matrix(C)
    elif isinstance(__value, Matrix):
      return self.__matmul__(__value)
    else:
      raise TypeError()

  def __imul__(self, __value: Matrix|int) -> Matrix:
    if isinstance(__value, int):
      for i in range(self.n):
        a = self.a[i]
        for j in range(self.m):
          a[j] *= __value
          if self._mod:
            a[j] %= _misaizu_lib_mod
      return self
    elif isinstance(__value, Matrix):
      return self.__matmul__(__value)
    else:
      raise TypeError

  def __pow__(self, n: int) -> Matrix:
    assert self.n == self.m, f""
    if not isinstance(n, int):
      raise TypeError

    sgn = 1 if n >= 0 else -1
    n = abs(n)

    C = Matrix.identity(self.n)
    a = Matrix([i[:] for i in self.a], mod=self._mod)
    while n:
      if n&1:
        C @= a
      a @= a
      n >>= 1
    return C if sgn == 1 else C.inv()

  def __ipow__(self, n: int) -> Matrix:
    assert self.n == self.m, f""
    if not isinstance(n, int):
      raise TypeError

    sgn = 1 if n >= 0 else -1
    n = abs(n)

    C = Matrix.identity(self.n)
    while n:
      if n&1:
        C @= self
      self @= self
      n >>= 1
    return C if sgn == 1 else C.inv()

  def __eq__(self, __value: object) -> bool:
    if isinstance(__value, Matrix):
      return self.a == __value.a
    else:
      return False

  def __neg__(self):
    return self.__mul__(-1)

  def __abs__(self):
    A = [[abs(j) for j in i] for i in self.a]
    return Matrix(A, self._mod)

  def __iter__(self):
    self.__iter = 0
    return self

  def __next__(self):
    if self.__iter == self.n:
      raise StopIteration
    self.__iter += 1
    return self.a[self.__iter-1]

  def transpose(self, inplace=False) -> Matrix|None:
    if inplace:
      self.a = list(map(list, zip(*self.a)))
      self.n, self.m = self.m, self.n
    else:
      a = self.a
      a = list(map(list, zip(*self.a)))
      return Matrix(a)

  def det(self) -> int:
    _force_det = False
    assert self.n == self.m, f""
    assert _force_det or self._mod, f"Calculation of the determinant without taking mods may produce float elements. Set _force_det to False to calculate the determinant."

    A = [a[:] for a in self.a]
    res = 1
    for i in range(self.m):
      a = A[i]
      if a[i] == 0:
        for j in range(i+1, self.n):
          if A[j][i]:
            break
        else:
          return 0
        A[i], A[j] = A[j], A[i]
        a = A[i]
        res = -res

      if self._mod:
        inv = pow(a[i], -1, _misaizu_lib_mod)
        for j in range(i+1, self.n):
          a_ = A[j]
          t = (a_[i]*inv)%_misaizu_lib_mod
          for k in range(i+1, self.m):
            a_[k] -= t*a[k]
            a_[k] %= _misaizu_lib_mod
      else:
        inv = a[i]
        for j in range(i+1, self.n):
          a_ = A[j]
          t = a_[i]/inv
          for k in range(i+1, self.m):
            a_[k] -= t*a[k]
    for i in range(self.n):
      res *= A[i][i]
      res %= _misaizu_lib_mod

    return res

  def inv(self, inplace=False):
    _force_inv = False
    assert self.n == self.m, f""
    assert _force_inv or self._mod, f"Calculation of the inverse matrix without taking mods may produce float elements. Set _force_inv to False to calculate the inverse matrix."

    n = self.n
    A = self.a if inplace else [i[:] for i in self.a]
    M = [[int(i==j) for j in range(n)] for i in range(n)]
    for i in range(n):
      a = A[i]
      m = M[i]
      if a[i] == 0:
        for j in range(i+1, n):
          if A[j][i] != 0:
            A[i], A[j] = A[j], A[i]
            a = A[i]
            M[i], M[j] = M[j], M[i]
            m = M[i]
            break
        else:
          raise AssertionError("The inverse matrix does not exist")

      if self._mod:
        tmp = pow(a[i], -1, _misaizu_lib_mod)
        for j in range(n):
          a[j] = a[j]*tmp%_misaizu_lib_mod
          m[j] = m[j]*tmp%_misaizu_lib_mod
        for j in range(n):
          if i == j:
            continue
          a_ = A[j]
          m_ = M[j]
          tmp = a_[i]
          for k in range(n):
            a_[k] = (a_[k] - a[k]*tmp)%_misaizu_lib_mod
            m_[k] = (m_[k] - m[k]*tmp)%_misaizu_lib_mod
      else:
        tmp = a[i]
        for j in range(n):
          a[j] /= tmp
          m[j] /= tmp
        for j in range(n):
          if i == j:
            continue
          a_ = A[j]
          m_ = M[j]
          tmp = a_[i]
          for k in range(n):
            a_[k] = a_[k] - a[k]*tmp
            m_[k] = m_[k] - m[k]*tmp
    return Matrix(M, mod=self._mod)
