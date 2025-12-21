def newton_root(f, df, x0, tol, max_iter):
    """
    Numerické hledání kořene funkce pomocí Newtonovy metody.

    :param f: Funkce, jejíž kořen hledáme
    :param df: Derivace funkce f
    :param x0: Počáteční odhad
    :param tol: Tolerance (přesnost)
    :param max_iter: Maximální počet iterací
    :return: Kořen funkce nebo None, pokud metoda selže
    """
    x = x0
    print(f"Initial guess x0={x0}, f(x0)={f(x0)}")
    for i in range(max_iter):
        fx = f(x)
        dfx = df(x)  # Derivace

        # Ochrana proti dělení nulou
        if abs(dfx) < 1e-12:
            print("Error: Derivace je nulová.")
            return None

        x_new = x - fx / dfx

        # Kontrola, zda jsme dosáhli dostatečné přesnosti
        if abs(x_new - x) < tol:
            return x_new
        x = x_new
    print("Error: Did not converge.")
    return None

# Příklad použití:
# root = newton_root(lambda x: x**2 - 4, lambda x: 2*x, 1.0, 1e-6, 100)
# print(f"Kořen je: {root}")