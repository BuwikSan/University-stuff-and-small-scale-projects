def euler_step(f, x0, y0, h, n):
    """
    Numerické řešení ODE pomocí Eulerovy metody.
    
    :param f: Funkce f(x, y) představující derivaci dy/dx
    :param x0: Počáteční hodnota x
    :param y0: Počáteční hodnota y
    :param h: Délka kroku
    :param n: Počet kroků
    :return: Pole hodnot y (vektor)
    """
    if n < 1:
        print("Error: Number of steps n must be >= 1.")
        return None

    # Vytvoříme pole o velikosti n+1 naplněné nulami
    ys = [0.0] * (n + 1)
    ys[0] = y0
    
    x = x0
    y = y0
    
    for i in range(1, n + 1):
        # Samotný Eulerův krok: y_nové = y_staré + h * sklon
        y = y + h * f(x, y)
        x = x + h
        ys[i] = y
    return ys

# Příklad použití:
# f = lambda x, y: x + y  (pro rovnici y' = x + y)
# vysledek = euler_step(f, 0, 1, 0.1, 10)