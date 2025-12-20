import math

def nonlinear_fit(p, a, am_min, am_max, b_min, b_max, am_step, b_step):
    """
    Nelineární regrese modelu a = (am * b * p) / (1 + b * p) metodou grid search.
    
    :param p: Nezávislá proměnná (tlak/koncentrace)
    :param a: Závislá proměnná (adsorpce/rychlost)
    :param am_min, am_max, am_step: Rozsah a krok pro parametr am
    :param b_min, b_max, b_step: Rozsah a krok pro parametr b
    :return: List [best_am, best_b]
    """
    best_err = float('inf')
    best_am = 0.0
    best_b = 0.0

    # Simulace vnořených cyklů z Go
    # Použijeme while, protože range v Pythonu neumí float kroky
    am = am_min
    while am <= am_max:
        b = b_min
        while b <= b_max:
            current_err = 0.0
            
            # Výpočet sumy čtverců chyb pro aktuální parametry
            for i in range(len(p)):
                # Model: Langmuirova rovnice
                model_val = (am * b * p[i]) / (1 + b * p[i])
                diff = a[i] - model_val
                current_err += diff * diff
            
            # Pokud jsme našli lepší shodu, uložíme si parametry
            if current_err < best_err:
                best_err = current_err
                best_am = am
                best_b = b
            
            b += b_step
        am += am_step

    return [best_am, best_b]