def gauss_pivot(a, b):
    """
    Řešení soustavy Ax = b pomocí Gaussovy eliminace s částečnou pivotací.
    """
    n = len(b)
    if n != len(a) or any(len(row) != n for row in a):
        print("Error: Mismatched lengths")
        return None

    # Vytvoření rozšířené matice (Bind)
    ab = []
    for i in range(n):
        ab.append(list(a[i]) + [b[i]])

    # 1. Přímý chod s pivotací
    for k in range(n - 1):
        # Hledání pivota (řádek s největší hodnotou v aktuálním sloupci)
        pivot_row = k
        max_val = abs(ab[k][k])
        for r in range(k + 1, n):
            if abs(ab[r][k]) > max_val:
                max_val = abs(ab[r][k])
                pivot_row = r

        # Prohození řádků v rozšířené matici
        if pivot_row != k:
            ab[k], ab[pivot_row] = ab[pivot_row], ab[k]

        # Samotná eliminace
        for i in range(k + 1, n):
            # Pokud by i po prohození byla na diagonále nula, soustava nemá jedno řešení
            if ab[k][k] == 0:
                print("Error: Matrix is singular")
                return None
                
            c = -ab[i][k] / ab[k][k]
            for j in range(k, n + 1):
                ab[i][j] += c * ab[k][j]

    # 2. Zpětná substituce
    x = [0.0] * n
    # Výpočet posledního x
    x[n - 1] = ab[n - 1][n] / ab[n - 1][n - 1]
    
    # Výpočet ostatních x směrem nahoru
    for i in range(n - 2, -1, -1):
        sum_val = 0.0
        for j in range(i + 1, n):
            sum_val += ab[i][j] * x[j]
        
        x[i] = (ab[i][n] - sum_val) / ab[i][i]
        
    return x