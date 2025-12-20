import math

def multiply_matrix_vector(a, x):
    """Pomocná funkce pro součin matice a vektoru (MulVec)"""
    n = len(a)
    ax = [0.0] * n
    for i in range(n):
        for j in range(len(a[i])):
            ax[i] += a[i][j] * x[j]
    return ax

def jacobi(a, b, max_iter, tol):
    """
    Řešení soustavy Ax = b pomocí Jacobiho iterativní metody.
    """
    n = len(a)
    if n != len(b) or any(len(row) != n for row in a):
        print("Error: Mismatched lengths")
        return None

    x = [0.0] * n   # Nové hodnoty
    x0 = [0.0] * n  # Hodnoty z předchozí iterace (k-té)

    for k in range(max_iter):
        for i in range(n):
            sum_val = 0.0
            # Všimni si: používáme výhradně hodnoty z x0
            for j in range(n):
                sum_val += a[i][j] * x0[j]
            
            if a[i][i] == 0:
                print("Error: Zero diagonal element")
                return None
            
            # Výpočet nové hodnoty x[i]
            # Vzorec: (b[i] - suma(A[i][j]*x0[j] pro j != i)) / A[i][i]
            # Tvůj Go kód to dělá šikovně: odečte sumu všech a pak přičte a[i][i]*x0[i]
            x[i] = (b[i] - sum_val + a[i][i] * x0[i]) / a[i][i]

        # Aktualizace x0 pro další iteraci (copy v Go)
        x0 = list(x)

        # Kontrola konvergence
        ax = multiply_matrix_vector(a, x0)
        
        # Kontrola na chyby (NaN/Inf)
        if any(math.isnan(v) or math.isinf(v) for v in ax):
            print("Error: Did not converge")
            return None

        # Výpočet rezidua (rozdílu od pravé strany)
        diff_sum = sum(abs(ax[i] - b[i]) for i in range(n))

        if diff_sum < tol:
            return x0

    print("Error: Did not converge")
    return None