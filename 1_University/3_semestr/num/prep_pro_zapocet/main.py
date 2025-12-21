# Numerická úloha: Najděte p takové, že
# \int_0^p \left( \int_0^{2\pi} e^{-alpha x \sin x} dx \right) d\alpha = 1.31848
# Použijeme Simpsonovo pravidlo pro integraci a bisekci pro hledání p

import math
from methods.integral.simpson import simpson_rule
from methods.koreny.bisekce import bisection
from methods.koreny.secant import secant


if __name__ == "__main__":
    target_value = 1.31848

    def inner_integral(alpha, n_x=1000):
        """
        Vnitřní integrál podle x: \int_0^{2pi} e^{-alpha x sin x} dx
        """
        def f(x):
            return math.exp(-alpha * x) * math.sin(x)
        return simpson_rule(f, 0, 2 * math.pi, n_x)

    p_start = 2
    outer_result = simpson_rule(inner_integral, 0, p_start, 1000)
    
    plow = 0.0
    phigh = 10.0
    tolerance = 1e-6
    max_iterations = 1000

    # Funkce pro hledání p pomocí secant metody
    def find_p_secant(target=target_value, x0=2.0, x1=10.0, tol=tolerance, n_x=1000):
        def h(p):
            return simpson_rule(inner_integral, 0, p, n_x) - target
        return secant(h, x0, x1, tol, max_iterations)

    # Výsledek bisekce
    bisection_result = bisection(
        lambda p: simpson_rule(inner_integral, 0, p, 1000) - target_value,
        plow,
        phigh,
        tolerance,
        max_iterations
    )
    print(f"Nalezené p (bisekce): {bisection_result}")
    if bisection_result is not None:
        print(f"Kontrola: hodnota integrálu = {simpson_rule(inner_integral, 0, bisection_result, 1000)}")

    # Výsledek secant metody
    secant_result = find_p_secant()
    print(f"Nalezené p (secant): {secant_result}")
    if secant_result is not None:
        print(f"Kontrola: hodnota integrálu = {simpson_rule(inner_integral, 0, secant_result, 1000)}")