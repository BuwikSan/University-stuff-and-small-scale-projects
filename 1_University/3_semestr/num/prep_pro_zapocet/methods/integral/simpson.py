def simpson_rule(f, a, b, n):
    """
    Numerický výpočet integrálu pomocí Simpsonova pravidla.
    
    :param f: Integrovaná funkce
    :param a: Dolní mez
    :param b: Horní mez
    :param n: Počet dělení (musí být sudé a >= 2)
    :return: Přibližná hodnota integrálu
    """
    # Simpson vyžaduje sudý počet intervalů (n+1 bodů)
    if n < 2 or n % 2 != 0:
        print("Error: Unsupported value for n. Must be even and >= 2.")
        return None

    h = (b - a) / n
    # Začneme součtem krajních hodnot f(a) + f(b)
    total_sum = f(a) + f(b)

    for i in range(1, n):
        x = a + i * h
        # Body v lichých pozicích se násobí 4, v sudých 2
        if i % 2 == 0:
            total_sum += 2 * f(x)
        else:
            total_sum += 4 * f(x)

    # Konečný vzorec: (h/3) * (f(a) + 4*f(x1) + 2*f(x2) + 4*f(x3) + ... + f(b))
    approximation = (h / 3) * total_sum

    return approximation