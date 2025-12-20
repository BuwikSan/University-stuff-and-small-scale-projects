def newton_interpolation(x, y):
    """
    Vypočítá koeficienty (poměrné diference) Newtonova interpolačního polynomu.
    
    :param x: Uzly interpolace (souřadnice x)
    :param y: Hodnoty v uzlech (souřadnice y)
    :return: Seznam koeficientů c0, c1, ..., cn
    """
    if len(x) == 0 or len(y) == 0:
        print("Error: Nil values are not supported.")
        return None
    
    if len(x) != len(y):
        print("Error: X and Y must have the same length.")
        return None

    n = len(x)
    # Inicializace koeficientů hodnotami y (copy v Go)
    coef = list(y)

    # Výpočet tabulky poměrných diferencí "v místě" (in-place)
    for i in range(1, n):
        # Postupujeme pozpátku, abychom si nepřepsali hodnoty, 
        # které ještě budeme potřebovat v té samé iteraci
        for j in range(n - 1, i - 1, -1):
            # Vzorec pro poměrnou diferenci: (f[x1...xk] - f[x0...xk-1]) / (xk - x0)
            denominator = x[j] - x[j - i]
            
            if denominator == 0:
                print("Error: Duplicate x values encountered (division by zero).")
                return None
                
            coef[j] = (coef[j] - coef[j - 1]) / denominator

    return coef