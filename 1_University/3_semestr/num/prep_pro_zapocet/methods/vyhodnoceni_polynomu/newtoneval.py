def newton_evaluation(t, x, coef):
    """
    Vyčíslení Newtonova interpolačního polynomu v bodech 't'.
    
    :param t: Body, ve kterých chceme zjistit hodnotu (hledané souřadnice x)
    :param x: Uzly interpolace (zadané souřadnice x)
    :param coef: Koeficienty (poměrné diference) polynomu
    :return: Seznam výsledných hodnot
    """
    if len(x) == 0 or len(coef) == 0 or len(t) == 0:
        print("Error: Nil values are not supported.")
        return None

    n = len(coef)
    m = len(t)
    
    # Inicializace výsledků hodnotou posledního koeficientu
    # Odpovídá prvnímu cyklu v Go: res[j] = coef[n-1]
    res = [coef[n - 1]] * m

    # Zpětný chod (obdoba Hornerova schématu)
    for i in range(n - 2, -1, -1):
        for j in range(m):
            # Vzorec: P(t) = c_i + (t - x_i) * P_příští(t)
            res[j] = res[j] * (t[j] - x[i]) + coef[i]
            
    return res