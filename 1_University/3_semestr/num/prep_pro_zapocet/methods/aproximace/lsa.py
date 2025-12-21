import math
from ..lin_rovnice.gausspivot import gauss_pivot

def lsa(x, y, n):
    """
    Aproximace dat polynomem stupně (n-1) pomocí metody nejmenších čtverců.
    
    :param x: Vstupní data (nezávislá proměnná)
    :param y: Naměřené hodnoty (závislá proměnná)
    :param n: Počet koeficientů polynomu (stupeň + 1)
    :return: Koeficienty polynomu [a0, a1, ..., an-1]
    """
    if len(x) == 0 or len(y) == 0:
        print("Error: Nil values are not supported.")
        return None

    if len(x) != len(y):
        print("Error: Mismatched lengths of X and Y.")
        return None

    if n <= 0:
        print("Error: Unsupported value for n.")
        return None

    # Inicializace matice A (n x n) a vektoru b (n)
    # Odpovídá matrix.NewMatrix(n) a make(vector.Vector2, n)
    A = [[0.0 for _ in range(n)] for _ in range(n)]
    b = [0.0] * n

    # Sestavení normální soustavy rovnic
    for i in range(n):
        # Naplnění matice soustavy (sumy mocnin x)
        for j in range(n):
            s = 0.0
            for k in range(len(x)):
                s += math.pow(x[k], float(i + j))
            A[i][j] = s
        
        # Naplnění pravé strany (sumy součinů y * x^i)
        s = 0.0
        for k in range(len(x)):
            s += y[k] * math.pow(x[k], float(i))
        b[i] = s

    # Vyřešení soustavy pomocí dříve definovaného Gausse s pivotací
    return gauss_pivot(A, b)