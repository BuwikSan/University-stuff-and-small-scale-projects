import math

def test_f(x):
    """Testovací funkce: x^2 * sin(x)"""
    return math.pow(x, 2) * math.sin(x)

def midpoint_rule(f, a, b, n):
    """
    Numerický výpočet určitého integrálu funkce f na intervalu [a, b].
    
    :param f: Integrovaná funkce
    :param a: Dolní mez
    :param b: Horní mez
    :param n: Počet dělení (obdélníků)
    :return: Přibližná hodnota integrálu
    """
    if n < 1:
        print("Error: Unsupported value for n. Must be n >= 1.")
        return None

    # Šířka jednoho obdélníku
    h = (b - a) / n
    total_sum = 0.0
    
    # Procházíme n podintervalů
    for i in range(1, n + 1):
        # Výpočet středu aktuálního obdélníku
        # a + (h * i) je pravý kraj, odečtením h/2 dostaneme střed
        midpoint = a + (h * i) - (h / 2)
        total_sum += f(midpoint)
    
    # Celkový obsah je šířka krát součet výšek
    approximation = h * total_sum
    return approximation

# Příklad použití:
# vysledek = midpoint_rule(test_f, 0, math.pi, 100)
# print(f"Integrál je přibližně: {vysledek}")