import math
from ..obecne_operace import multiply_matrix_vector


def gauss_seidel(a, b, max_iter, tol):
    """
    Řešení soustavy Ax = b iterativní Gauss-Seidelovou metodou.
    """
    n = len(b)
    if n != len(a) or any(len(row) != n for row in a):
        print("Error: Mismatched lengths")
        return None

    # Počáteční odhad (vektor nul)
    x = [0.0] * n

    for iter_idx in range(max_iter):
        for i in range(n):
            sum_val = 0.0
            for k in range(len(a[i])):
                if k != i:
                    sum_val += a[i][k] * x[k]
            
            if a[i][i] == 0:
                print("Error: Zero diagonal element in GaussSeidel")
                return None
            
            # Výpočet nové složky x[i] (okamžitě se použije pro další i v této iteraci)
            x[i] = (b[i] - sum_val) / a[i][i]

        # Kontrola konvergence (podle rezidua Ax - b)
        ax = multiply_matrix_vector(a, x)
        
        # Kontrola na NaN a Inf (pokud metoda diverguje)
        for v in ax:
            if math.isnan(v) or math.isinf(v):
                print("Error: Did not converge (diverged to NaN/Inf)")
                return None

        # Výpočet sumy absolutních rozdílů (L1 norma rezidua)
        residual_sum = 0.0
        for i in range(len(ax)):
            residual_sum += abs(ax[i] - b[i])

        # Pokud je chyba menší než tolerance, máme hotovo
        if residual_sum < tol:
            return x

    print("Error: Did not converge within max iterations")
    return None