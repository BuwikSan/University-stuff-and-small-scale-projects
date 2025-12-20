def lagrange(t, x, y):
    """
    Lagrangeova interpolace.
    
    :param t: Body, ve kterých chceme interpolovat (zjistit hodnotu na křivce)
    :param x: Zadané souřadnice x (uzly interpolace)
    :param y: Zadané souřadnice y
    :return: Seznam interpolovaných hodnot v bodech t
    """
    if len(x) != len(y):
        print("Error: Mismatched lengths for x and y.")
        return None

    ln = len(x)
    lt = len(t)

    if ln == 0 or lt == 0:
        print("Error: Nil values are not supported.")
        return None

    # Inicializace výsledného seznamu (odpovídá make(vector.Vector2, lt))
    res = [0.0] * lt

    # Pro každý bod 'k' v t, kde chceme znát výsledek
    for k in range(lt):
        current_sum = 0.0
        # Procházíme všechny zadané body (uzly) i
        for i in range(ln):
            m = 1.0
            # Výpočet bázického polynomu L_i(t_k)
            for j in range(ln):
                if j != i:
                    # Hlavní vzorec Lagrangeova polynomu
                    m *= (t[k] - x[j]) / (x[i] - x[j])
            
            # Přičtení y_i * L_i k celkové sumě
            current_sum += y[i] * m
        
        res[k] = current_sum
        
    return res