import math

def bisection(f, a, b, tol, max_iter):
    """
    Numerické hledání kořene funkce pomocí metody půlení intervalu.
    
    :param f: Funkce, jejíž kořen hledáme
    :param a: Levá mez intervalu
    :param b: Pravá mez intervalu
    :param tol: Tolerance (přesnost)
    :param max_iter: Maximální počet iterací
    :return: Kořen funkce nebo None, pokud metoda selže
    """
    fa = f(a)
    fb = f(b)
    print(f"Initial f(a)={fa}, f(b)={fb}")

    # Kontrola, zda v intervalu vůbec může být kořen (změna znaménka)
    if fa * fb > 0:
        print("Error: No sign change, can't guarantee a root.")
        return None

    c = a
    for i in range(max_iter):
        c = (a + b) / 2
        fc = f(c)

        # Kontrola, zda jsme dosáhli dostatečné přesnosti
        if abs(fc) < tol or (b - a) / 2 < tol:
            return c

        # Rozhodnutí, kterou polovinu intervalu si ponecháme
        if fa * fc < 0:
            b = c
            fb = fc
        else:
            a = c
            fa = fc

    print("Error: Did not converge.")
    return None

# Příklad použití:
# root = bisection(lambda x: x**2 - 4, 0, 5, 1e-6, 100)
# print(f"Kořen je: {root}")