def gauss(a, b):
    """
    Řešení soustavy lineárních rovnic Ax = b pomocí Gaussovy eliminace.
    """
    n = len(b)
    
    # Kontrola rozměrů (čtvercová matice)
    if n != len(a) or any(len(row) != n for row in a):
        print("Error: Mismatched lengths")
        return None

    # Vytvoření rozšířené matice (Bind v Go)
    # V Pythonu vytvoříme kopii, abychom nezměnili původní data
    ab = []
    for i in range(n):
        ab.append(list(a[i]) + [b[i]])

    # 1. Přímý chod (vytvoření horní trojúhelníkové matice)
    for k in range(n - 1):
        # Poznámka: V praxi by zde měl být "pivoting" (prohození řádků), 
        # aby ab[k][k] nebylo nula.
        for i in range(k + 1, n):
            c = -ab[i][k] / ab[k][k]
            for j in range(k, n + 1):
                ab[i][j] += c * ab[k][j]

    # 2. Zpětný chod (výpočet hodnot neznámých x)
    x = [0.0] * n
    for i in range(n - 1, -1, -1):
        sum_val = ab[i][n]
        for j in range(i + 1, n):
            sum_val -= ab[i][j] * x[j]
        
        x[i] = sum_val / ab[i][i]
        
    return x