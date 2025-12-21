def secant(f, x0, x1, tol=1e-8, max_iter=100):
    """
    Numerické hledání kořene funkce pomocí metody sečen (secant method).

    :param f: Funkce, jejíž kořen hledáme
    :param x0: První počáteční odhad
    :param x1: Druhý počáteční odhad
    :param tol: Tolerance (přesnost)
    :param max_iter: Maximální počet iterací
    :return: Kořen funkce nebo None, pokud metoda selže
    """
    print(f"Initial guesses x0={x0}, f(x0)={f(x0)}; x1={x1}, f(x1)={f(x1)}")
    for i in range(max_iter):
        fx0 = f(x0)
        fx1 = f(x1)
        # Ochrana proti dělení nulou
        if abs(fx1 - fx0) < 1e-12:
            print("Error: Rozdíl funkčních hodnot je příliš malý.")
            return None
        x2 = x1 - fx1 * (x1 - x0) / (fx1 - fx0)
        print(f"Iter {i}: x0={x0}, x1={x1}, x2={x2}, f(x2)={f(x2)}")
        # Kontrola, zda jsme dosáhli dostatečné přesnosti
        if abs(x2 - x1) < tol:
            return x2
        x0, x1 = x1, x2
    print("Error: Did not converge.")
    return None

# Příklad použití:
# root = secant(lambda x: x**2 - 4, 0, 3, 1e-6, 100)
# print(f"Kořen je: {root}")