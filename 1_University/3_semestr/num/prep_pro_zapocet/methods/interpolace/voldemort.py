from ..lin_rovnice.gausspivot import gauss_pivot

def vandermonde(x, y):
    """
    Interpolace pomocí Vandermondovy matice.
    Vrací koeficienty polynomu [a0, a1, ..., an-1].
    """
    if len(x) == 0 or len(y) == 0:
        print("Error: Nil values are not supported.")
        return None
    
    if len(x) != len(y):
        print("Error: X and Y must have the same length.")
        return None

    n = len(x)
    
    # Vytvoření matice n x n naplněné jedničkami
    # Odpovídá matrix.NewMatrix(n) a A.Fill(1)
    a_matrix = [[1.0 for _ in range(n)] for _ in range(n)]

    # Naplnění matice: každý sloupec j je i-tý prvek umocněný na j
    # Využíváme efektivní násobení předchozím prvkem místo math.pow
    for j in range(1, n):
        for i in range(n):
            a_matrix[i][j] = a_matrix[i][j - 1] * x[i]

    # Vyřešení soustavy Va = y pomocí Gausse s pivotací
    # Výsledkem jsou koeficienty a0, a1, ... an-1
    return gauss_pivot(a_matrix, y)