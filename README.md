# OR

Consider the problem of assigning $m$ items to $n$ groups.
```math
X = \begin{pmatrix}
x_{11} & x_{12} & \cdots & x_{1n} \\
x_{21} & x_{22} & \cdots & x_{2n} \\
\vdots & \vdots & \vdots & \vdots \\
x_{m1} & x_{m2} & \cdots & x_{mn}
\end{pmatrix},
Y = \begin{pmatrix}
y_{11} & y_{12} & \cdots & y_{1p} \\
y_{21} & y_{22} & \cdots & y_{2p} \\
\vdots & \vdots & \vdots & \vdots \\
y_{n1} & y_{n2} & \cdots & y_{np}
\end{pmatrix},
C = \begin{pmatrix}
c_{11} & c_{12} & \cdots & c_{1p} \\
c_{21} & c_{22} & \cdots & c_{2p} \\
\vdots & \vdots & \vdots & \vdots \\
c_{n1} & c_{n2} & \cdots & c_{np}
\end{pmatrix}
```
$x_{ij}$ represents the assignment of item $i$ to group $j$, $y_{jk}$ represents the removal of property $k$ from group $j$ and $c_{jk}$ is the cost of doing so.

The objective is to minimize
```math
\sum_{j=1}^n\sum_{k=1}^p c_{jk} * y_{jk}
```
subject to the following constraints
```math
\tag{1} \sum_{j=1}^n x_{ij} = 1, i = 1,...,m
```
```math
\tag{2} \sum_{i=1}^m x_{ij} \ge N_j, j = 1,...,mn
```
```math
\tag{3} \sum_{i=1}^m x_{ij} * (1 - y_{jk}) * \lambda_{ik}^{(2)} \ge 1 - y_{jk}, j = 1,...,n, k = 1,...,p, \kappa_{jk} = 1
```
```math
\tag{4} y_{jk} \le \kappa_{jk}, j = 1,...,n, k = 1,...,p
```
given that $N_j$ is the minimum size of the groups, $\lambda_{ik}^{(2)}$ is a matrix indicating 1 if property $k$ of item $i$ as a level above 2 and $\kappa_{jk}$ is a matrix indicating if group $j$ requires property $k$.