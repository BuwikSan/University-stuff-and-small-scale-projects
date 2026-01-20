import math
from matplotlib import pyplot as plt

def příklad():
    # Importy funkcí z tvého projektu; tyto moduly jsou v adresáři `methods/`
    from methods.dif_rovnice.eulerstep import euler_step
    from methods.interpolace.newtoninterpolation import newton_interpolation
    from methods.obecne_operace import make_linspace
    from methods.lin_rovnice.gauss import gauss

    # Počáteční hodnota N (populace / stav)
    N_0 = 60


    def allee(N, t):
        # parametrika modelu:
        r = 0.5  
        A = 20   
        K = 100  


        t = -r * N * (1 - (N / A)) * (1 - (N / K))
        return t


    vysledky_derivace = euler_step(allee, 0, N_0, 0.1, 500)

    # Rychlý graf celé trajektorie (jen pro kontrolu)
    plt.plot(vysledky_derivace)
    plt.show()


    # Najdi první index, kde hodnota překročí 80

    for i in range(len(vysledky_derivace)):
        if vysledky_derivace[i] > 80:
            # dva_body = ((index_prev, index_curr), (value_prev, value_curr))
            dva_body = ((i - 1, i), (vysledky_derivace[i - 1], vysledky_derivace[i]))
            break
    print(dva_body)

    # Aproximuj průsečík lineární (nebo Newtonovou) interpolací

    # newton_interpolation pravděpodobně vrací koeficienty polynomu (např. [c0, c1])
    t_k_aprox = newton_interpolation(dva_body[0], dva_body[1])
    print(t_k_aprox)

    # Krátká funkce pro vygenerování hodnot z nalezené přímky
    def linf(x, t_k):
        # očekává t_k ve formě [c0, c1]
        return t_k[0] + t_k[1] * x

    # Vygeneruj hustou mřížku x v intervalu [0.7, 0.85] (200k bodů)
    # a spočti odpovídající hodnoty přímky.
    linf_gen = [linf(i, t_k_aprox) for i in make_linspace(0.7, 0.85, 200000)]

    # ------------------------
    # Najdi bod v linf_gen, který je blízko 80 (tolerance)
    # ------------------------
    def najdi_bod_blizko(tol, vector, ceho):
        # prochází pole a vrátí index, kde je vector[i] v intervalu
        # (ceho - tol, ceho + tol). Pokud nic nenajde, vypíše "tak nic".
        for i in range(len(vector)):
            if vector[i] > ceho - tol and vector[i] < ceho + tol:
                return i
        else:
            print("tak nic")
            # implicitně vrací None

    x_plus = najdi_bod_blizko(0.00001, linf_gen, 80)


    # Toto místo je křehké: ověř, co přesně newton_interpolation vrací.
    t_k = float(make_linspace(0.7, 0.85, 200000)[x_plus]) + float(t_k_aprox[0])
    print(t_k)

    # Zobrazit graf přímky vs osy (jen vizuální kontrola)
    plt.plot(linf_gen, make_linspace(0.7, 0.85, 200000))
    plt.show()

    # ------------------------
    # Přesnější postup: spočítat tk pro různé dt a fitnout závislost tk(dt)
    # ------------------------
    # Předpoklad: chceme páry (dt, tk) a potom kvadratickou regresí/extrapolací
    # získat hodnotu tk při dt -> 0 (to je intercept c).
    N0 = 60.0
    threshold = 80.0

    # Funkce, která z trajektorie (pole hodnot) získá přesnější crossing time
    # pomocí lineární interpolace mezi sousedními body.
    def tk_from_traj(traj, dt):
        for i in range(1, len(traj)):
            a, b = traj[i - 1], traj[i]
            # test převýšení threshold vzestupně nebo sestupně
            if (a < threshold <= b) or (a > threshold >= b):
                t0 = (i - 1) * dt
                # pokud jsou hodnoty stejné, nelze interpolovat (vracíme t0)
                if b == a:
                    return t0
                # lineární interpolace: portion mezi kroky, kdy dojde k průsečíku
                frac = (threshold - a) / (b - a)
                # přesný čas průsečíku
                return t0 + frac * dt
        # threshold nebyl dosažen v trajektorii
        return None

    # Seznam dt (od hrubého po jemné) — uprav podle potřeby
    dt_values = [0.5, 0.25, 0.1, 0.05, 0.02, 0.01]
    pairs = []

    # Pro každý dt spustíme Euler a najdeme tk
    for dt in dt_values:
        # max_steps zvoleno jako celkový čas 200 / dt (tzn. integrujeme do t~200)
        max_steps = int(200.0 / dt)
        traj = euler_step(allee, 0.0, N0, dt, max_steps)
        # POZOR: pokud máš problém s pořadím parametrů v allee, traj bude nesmyslný
        tk = tk_from_traj(traj, dt)
        print("dt =", dt, "tk =", tk)
        if tk is not None:
            pairs.append((dt, tk))

    # Potřebujeme alespoň 3 bodu pro quadratickou regresi (stupeň 2)
    if len(pairs) < 3:
        raise SystemExit("Need >=3 points for quadratic fit; increase max_steps or add dt values.")

    # ------------------------
    # Sestav normalni rovnice pro kvadratickou regrese:
    # Minimalizujeme sum_i (y_i - (a*dt_i^2 + b*dt_i + c))^2
    # => 3x3 soustava pro (a,b,c)
    # ------------------------
    S = {
        'dt4': 0.0, 'dt3': 0.0, 'dt2': 0.0, 'dt1': 0.0, '1': 0.0,
        'y_dt2': 0.0, 'y_dt': 0.0, 'y': 0.0
    }
    # Sčítání potřebných součtů
    for dt, y in pairs:
        d2 = dt * dt
        d3 = d2 * dt
        d4 = d2 * d2
        S['dt4'] += d4
        S['dt3'] += d3
        S['dt2'] += d2
        S['dt1'] += dt
        S['1'] += 1.0
        S['y_dt2'] += y * d2
        S['y_dt'] += y * dt
        S['y'] += y

    # Matice normálních rovnic Ax = B, kde x = [a, b, c]
    A = [
        [S['dt4'], S['dt3'], S['dt2']],
        [S['dt3'], S['dt2'], S['dt1']],
        [S['dt2'], S['dt1'], S['1']]
    ]
    B = [S['y_dt2'], S['y_dt'], S['y']]

    # Řešení 3x3 soustavy pomocí tvé funkce gauss (bez numpy) — vrátí [a,b,c]
    # Upozornění: gauss() v projektu neprovádí pivoting; pokud bude při výpočtu dělení
    # nulou, může být potřeba upravit data nebo implementovat pivoting.
    a, b, c = gauss(A, B)
    print("fit a,b,c =", a, b, c)
    # Extrapolovaná hodnota při dt->0 je c (hodnota polynomu v 0)
    print("extrapolated tk at dt->0 =", c)
    


if __name__ == "__main__":
    příklad()
    