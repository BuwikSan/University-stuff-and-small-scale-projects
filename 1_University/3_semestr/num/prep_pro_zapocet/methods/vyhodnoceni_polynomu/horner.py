def horner(t, coefs):
    """
    Vyčíslení polynomu v bodech 't' pomocí Hornerova schématu.
    
    :param t: Seznam bodů (x), ve kterých chceme znát hodnotu
    :param coefs: Koeficienty polynomu od nejnižší mocniny po nejvyšší 
                  (např. [5, 2, 3] pro 3x^2 + 2x + 5)
    :return: Seznam výsledných hodnot
    """
    if not t or not coefs:
        print("Error: Nil values are not supported.")
        return None

    # Vytvoříme výsledné pole stejné délky jako t
    res = [0.0] * len(t)
    
    # Pro každý bod v t vypočítáme hodnotu polynomu
    for i in range(len(t)):
        # Začneme od koeficientu u nejvyšší mocniny
        acc = coefs[len(coefs) - 1]
        
        # Postupně násobíme bodem t[i] a přičítáme další koeficienty směrem dolů
        for j in range(len(coefs) - 2, -1, -1):
            acc = acc * t[i] + coefs[j]
            
        res[i] = acc
        
    return res