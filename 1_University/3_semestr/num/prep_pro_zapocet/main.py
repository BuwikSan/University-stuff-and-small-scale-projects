import math
from matplotlib import pyplot as plt

def příklad1():
    from methods.integral.simpson import simpson_rule
    from methods.koreny.bisekce import bisection
    from methods.koreny.secant import secant
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

def příklad2(N):
    from methods.lin_rovnice.gausspivot import gauss_pivot
    from methods.interpolace.lagrange import lagrange
    from methods.obecne_operace import make_matrix, make_linspace
    # matrix = []
    # j = range(1, N+1)
    # for row in i:
    #     matrix.append([])
    #     for col in j:
    #         matrix[row-1].append(1-(1/(row+col-1)))
    matrix = make_matrix(N, lambda i, j: 1 - (1 / (i + 1 + j + 1 - 1)))
    i = range(1, N+1)
    
    gauss_result = gauss_pivot(matrix, [1]*(N))
    lagrange_dimension_x = make_linspace(1, N, 1000)
    interpolovane_hodnoty = lagrange(lagrange_dimension_x, i, gauss_result)

    #střední hodnoty pro jednotlivé dimenze
    # stredni_hodnoty = []
    # for _ in range(N*2):
    #     rozmezi = (_ * len(interpolovane_hodnoty)/N, (_ + 1) * len(interpolovane_hodnoty)/N)
    #     sum = 0
    #     for x in rozmezi:
    #         sum+=interpolovane_hodnoty[int(x-1 )]
    #     stredni_hodnoty.append(sum / len(rozmezi))
    # print("Střední hodnoty pro jednotlivé dimenze:")    
    # print(stredni_hodnoty)
    střední_hodnoty = []
    for k in range(1, N):
        střední_hodnoty.append(lagrange([k+0.5], i, gauss_result)[0])
    print("Střední hodnoty pro jednotlivé dimenze:")
    print(střední_hodnoty)
    plt.plot(range(1, N), střední_hodnoty)
    plt.show()
    plt.plot(lagrange_dimension_x ,interpolovane_hodnoty)
    plt.show()

def příklad3():
    from methods.aproximace.lsa import lsa
    def f(x):
        return 1/x
    výpočty_po_dílkách = []
    for i in range(21):
        from methods.integral.simpson import simpson_rule
        výpočty_po_dílkách.append(simpson_rule(f, 1, 2, 2**i))
 
    def zavislost(integrace):
        analiticke_reseni = math.log(2)
        return abs(integrace - analiticke_reseni)

    zavislost_list = []
    for i in range(len(výpočty_po_dílkách)):
        if výpočty_po_dílkách[i] != None:
            zavislost_list.append(zavislost(výpočty_po_dílkách[i]))
        else:
            zavislost_list.append(None)

    print(zavislost_list)
    plt.plot(range(0, 21), zavislost_list)
    plt.show()

    aproximovane = lsa([i for i in range(1, 21)], zavislost_list[1:21], 3)
    print(aproximovane)

    predesly_vysledek = None
    kolikaty_vysledek = 1
    for vysledek in [aproximovane[0] + aproximovane[1]*i + aproximovane[2]*i**2 for i in range(1, 21)]:
        print(predesly_vysledek, vysledek, kolikaty_vysledek)
        if predesly_vysledek is not None:
            if vysledek > predesly_vysledek:
                print("Chyba: Hodnoty rostou!")
                print(vysledek, predesly_vysledek, kolikaty_vysledek)
                break
        predesly_vysledek = vysledek
        kolikaty_vysledek += 1

    plt.plot(range(1, 21), [aproximovane[0] + aproximovane[1]*i + aproximovane[2]*i**2 for i in range(1, 21)])
    plt.show()

def příklad4():
    from methods.obecne_operace import make_matrix
    from methods.integral.simpson import simpson_rule
    from methods.lin_rovnice.gausspivot import gauss_pivot
    def f(t, i, j):
        return t**(i+j-2)
    integrovana_fce = lambda i, j: simpson_rule(lambda t: f(t, i, j), 0, 1, 100)

    N = 20
    for n in range(1, N+1):
        A = make_matrix(n, lambda i, j: integrovana_fce(i+1, j+1))

        b = []
        for i in range(n):
            b.append(sum([A[i][j] for j in range(n)]))

        print(f"\nřád N={n}:")
        print("Matrix A:")
        for row in A:
            print(row)
        print("b:", b)
        x = gauss_pivot(A, b)
        print(f"\nŘešení x:", x)

def příklad5():
    from methods.aproximace.nonlinearregression import nonlinear_fit
    from methods.interpolace.lagrange import lagrange
    from methods.obecne_operace import make_linspace
    p = [0.1, 0.2, 0.28, 0.41, 0.98, 1.39, 1.93, 2.75, 3.01, 3.51]
    a = [0.089, 0.127, 0.144, 0.163, 0.189, 0.198, 0.206, 0.208, 0.209, 0.210]
    plt.plot(p, a, 'o', label='Data body')
    plt.show()

    def analiticka_zavislost(p, a_m, b):
        a = a_m*((b*p)/(1+b*p))
        return a
    
    am_min, am_max, am_step = 0.1, 0.3, 0.0001
    b_min, b_max, b_step = 0.1, 2.0, 0.001

    a_m, b = nonlinear_fit(
        p,
        a,
        am_min, am_max,
        b_min, b_max, 
        am_step, b_step
    )
    p
    interpolovane = lagrange([i/100 for i in range(0, 360)], p, a)

    p_fit = make_linspace(min(p), max(p), 200)
    a_fit = [analiticka_zavislost(val, a_m, b) for val in p_fit]

    plt.plot(p, a, 'o', label='Data')
    plt.plot(p_fit, a_fit, label='Analytický fit')
    plt.plot([i/100 for i in range(0, 360)], interpolovane, label='Lagrangeova interpolace')
    plt.legend()
    plt.show()

    for i in range(p_fit):
        if i == 0:
            last_aprox = a_fit[i]
            last_interp = interpolovane[i]
            pruseciky = []
            pass
        else:
            current_aprox = a_fit[i]
            current_interp = interpolovane[i]
            if ((last_aprox > last_interp) and (current_aprox < current_interp)) or ((last_aprox < last_interp) and (current_aprox > current_interp)):
                pruseciky.append((i, current_interp))
    
    print(pruseciky)
    
        

if __name__ == "__main__":
    příklad1()
    # příklad2(10)
    # příklad2(20)
    # příklad3()
    # příklad4()
    # příklad5()