def multiply_matrix_vector(a, x):
    """Pomocná funkce simulující matrix.MulVec(a, x)"""
    n = len(a)
    ax = [0.0] * n
    for i in range(n):
        for j in range(len(a[i])):
            ax[i] += a[i][j] * x[j]
    return ax

def transpose(a):
    """Transpozice matice."""
    return [[a[j][i] for j in range(len(a))] for i in range(len(a[0]))]

def multiply_matrices(a, b):
    """Násobení dvou matic."""
    rows_a, cols_a = len(a), len(a[0])
    rows_b, cols_b = len(b), len(b[0])
    res = [[0.0 for _ in range(cols_b)] for _ in range(rows_a)]
    for i in range(rows_a):
        for j in range(cols_b):
            for k in range(cols_a):
                res[i][j] += a[i][k] * b[k][j]
    return res

def make_matrix(řád, funkce_pro_doplnění_hodnot):
    """Vytvoří matici daného řádu a naplní ji hodnotami z funkce."""
    matice = []
    for i in range(řád):
        řádek = []
        for j in range(řád):
            řádek.append(funkce_pro_doplnění_hodnot(i, j))
        matice.append(řádek)
    return matice