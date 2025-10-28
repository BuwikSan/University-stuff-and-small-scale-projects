import numpy as np

class Aproximace_korenu():
    def __init__(self):
        pass

    def bisekce(self, f, a, b, eps=0.0000000001, max_iter=1000):
        if f(a)*f(b) > 0:
            raise Exception("Funkce nemá v intervalu kořen")
        
        iterace = 0
        while abs(b-a) > eps and iterace < max_iter:
            c = (a+b)/2
            if f(c) == 0:
                return c
            elif f(a)*f(c) < 0:
                b = c
            else:
                a = c
            iterace += 1

        if iterace == max_iter:
            raise Exception("Nekonverguje v rozumném počtu iterací")
        else:
            return (a+b)/2
        
    def regula_falsi(self, f, a, b, eps=0.0000001, max_iter=100000): 
        #pěkně na piču když kořen je zároveň inflexní bod to řeší třeba varianty Illinois, Pegasus, nebo Anderson-Björk
        if f(a)*f(b) > 0:
            raise Exception("Funkce nemá v intervalu kořen")
        
        iterace = 0
        while abs(b-a) > eps and iterace < max_iter:
            c = (a*f(b) - b*f(a)) / (f(b) - f(a))
            if abs(f(c)) < eps:  # Oprava: kontrola na malou hodnotu místo přesné nuly
                return c
            elif f(a)*f(c) < 0:
                b = c
            else:
                a = c
            iterace += 1
        # Oprava: přidán návrat nejlepší aproximace
        if iterace == max_iter:
            print("Nekonverguje v rozumném počtu iterací, ale vracím nejlepší aproximaci")
            return (a+b)/2
        else:
            return (a+b)/2

    def newton(self, f, fd, x0, eps=0.0000000001, max_iter=1000):
        iterace = 0
        while iterace < max_iter:
            x = x0 - f(x0)/fd(x0)
            if abs(x - x0) < eps:
                return x
            x0 = x
            iterace += 1

        if iterace == max_iter:
            raise Exception("Nekonverguje v rozumném počtu iterací")
        else:
            return x
        
    def halley(self, f, fd, fdd, x0, eps=0.0000000001, max_iter=1000):
        iterace = 0
        while iterace < max_iter:
            numerator = f(x0) * fd(x0)
            denominator = fd(x0)**2 - 0.5 * f(x0) * fdd(x0)  # Oprava: správný vzorec
            if denominator == 0:
                raise Exception("Denominator in Halley's method became zero.")
            x = x0 - numerator / denominator
            if abs(x - x0) < eps:
                return x
            x0 = x
            iterace += 1

        if iterace == max_iter:
            raise Exception("Nekonverguje v rozumném počtu iterací")
        else:
            return x

    def fixed_point(self, g, x0, eps=0.001, max_iter=10000, max_abs=1e6, min_abs=1e-12):
        xs = [x0]
        for i in range(max_iter):
            x1 = g(xs[-1])
            if abs(x1) > max_abs or abs(x1) < min_abs or np.isnan(x1) or np.isinf(x1):
                print(f"Divergence nebo nedefinovaná hodnota v iteraci {i+1}!")
                break
            xs.append(x1)
            if abs(x1 - xs[-2]) < eps:
                break
        return xs[-1]

    def newton_horner(self, poly, x0, tol=0.000001, max_iter=10000):
        def horner(poly, x):
            """
            poly: koeficienty polynomu [a0, a1, ..., an] (od nejnižšího)
            x: bod, kde vyhodnocujeme
            Vrací: (hodnota polynomu, hodnota derivace)
            """
            n = len(poly) - 1
            p = poly[n]
            dp = 0
            for i in range(n-1, -1, -1):
                dp = dp * x + p
                p = p * x + poly[i]
            return p, dp

        x = x0
        for i in range(max_iter):
            p, dp = horner(poly, x)
            if abs(dp) < 1e-14:
                print("Derivace je příliš malá, metoda selhává.")
                return x
            x_new = x - p / dp
            if abs(x_new - x) < tol:
                return x_new
            x = x_new
        print("Nekonverguje v rozumném počtu iterací")
        return x
    
class reseni_soustav_lin_rovnic:
    def __init__(self):
        pass

    def gauss_s_pivotováním(self, matice_A, vektor_řešení):
        Ab = np.column_stack((matice_A.astype(float), vektor_řešení.astype(float)))
        N = len(matice_A)
        # přímý chod
        for i in range(N - 1):
                # Pivotování
            if abs(Ab[i, i]) < 1e-12:
                for r in range(i+1, N):
                    if abs(Ab[r, i]) > 1e-12:
                        Ab[[i, r], :] = Ab[[r, i], :]
                        break
                else:
                    raise Exception("Nelze eliminovat: nulový pivot a žádný vhodný řádek k výměně.")
            for j in range(i+1, N):
                u = - Ab[j, i]/Ab[i, i]
                for k in range(i, N+1):  # Od aktuálního sloupce až po pravou stranu
                    Ab[j, k] = Ab[j, k] + u * Ab[i, k]

        # zpětný chod
        x = np.zeros(N)
        x[N-1] = Ab[N-1, N]/Ab[N-1, N-1]
        for k in range(N-2, -1, -1):
            x[k] = (Ab[k, N] - sum(Ab[k, j] * x[j] for j in range(k+1, N))) / Ab[k, k]
        return x

    def lu_rozklad(self, matice_A, vektor_řešení):
        N = len(matice_A)
        L = np.eye(N)
        U = matice_A.copy().astype(float)
        for k in range(N):
            for i in range(k+1, N):
                L[i, k] = U[i, k] / U[k, k]
                U[i, k:] = U[i, k:] - L[i, k] * U[k, k:]
        # Řešení Ly = b
        y = np.zeros(N)
        for i in range(N):
            y[i] = vektor_řešení[i] - sum(L[i, j] * y[j] for j in range(i))
        # Řešení Ux = y
        x = np.zeros(N)
        for i in range(N-1, -1, -1):
            x[i] = (y[i] - sum(U[i, j] * x[j] for j in range(i+1, N))) / U[i, i]
        return x

    def jacobiova(self, matice_A, vektor_řešení, eps=0.00001, max_iter=100):
        N = len(matice_A)
        x = np.zeros(N)
        for _ in range(max_iter):  # max počet iterací
            x_new = np.copy(x)
            for i in range(N):
                s = sum(matice_A[i, j] * x[j] for j in range(N) if j != i)
                x_new[i] = (vektor_řešení[i] - s) / matice_A[i, i]
            if np.linalg.norm(x_new - x) < eps:
                return x_new
            x = x_new
        raise Exception("Jacobiova metoda nekonverguje")

    def gauss_seidelova(self, matice_A, vektor_řešení, eps=0.00001, max_iter=100000):
        N = len(matice_A)
        x = np.zeros(N)
        for _ in range(max_iter):  # max počet iterací
            x_old = x.copy()
            for i in range(N):
                s = sum(matice_A[i, j] * x[j] for j in range(N) if j != i)
                x[i] = (vektor_řešení[i] - s) / matice_A[i, i]
            if np.linalg.norm(x - x_old) < eps:
                return x
        raise Exception("Gauss-Seidelova metoda nekonverguje")

class lin_interpolace:
    def __init__(self):
        pass
    
    def newton_linear(self, x_points, y_points, x):
        # Najdi interval, kam x patří
        for k in range(len(x_points) - 1):
            if x_points[k] <= x <= x_points[k+1]:
                # Newtonův tvar pro lineární interpolaci
                return y_points[k] + (x - x_points[k]) * (y_points[k+1] - y_points[k]) / (x_points[k+1] - x_points[k])
        raise ValueError("x je mimo rozsah zadaných bodů")

    def lagrange_linear(self, x_points, y_points, x):
        """
        Lagrangeova lineární interpolace po částech (piecewise linear).
        x_points: uzlové body (seřazené)
        y_points: hodnoty v uzlových bodech
        x: bod, kde interpolujeme
        """
        for k in range(len(x_points) - 1):
            if x_points[k] <= x <= x_points[k+1]:
                # Lagrangeův lineární polynom mezi dvěma body
                return y_points[k] + (x - x_points[k]) * (y_points[k+1] - y_points[k]) / (x_points[k+1] - x_points[k])
        raise ValueError("x je mimo rozsah zadaných bodů")

class polynom_interpolace:
    def __init__(self):
        pass

class aproximace:
    def __init__(self):
        pass

class num_der_a_int:
    def __init__(self):
        pass

class solve_odr:
    def __init__(self):
        pass



def main():
    aproximator_korenu = Aproximace_korenu()
    reseni_soustav_lin = reseni_soustav_lin_rovnic()
    print("věř mi, něco se stalo")
    print(aproximator_korenu.bisekce(lambda x: x*x*x, -2, 8))
    print(aproximator_korenu.regula_falsi(lambda x: x*x*x, -2, 3))
    print(aproximator_korenu.newton(lambda x: x*x*x, lambda x: 3*x*x, 10))
    print(aproximator_korenu.halley(lambda x: x*x*x, lambda x: 3*x*x, lambda x: 6*x, 10))
    print(aproximator_korenu.fixed_point(lambda x: 1/(x**2), 10))
    print(aproximator_korenu.newton_horner([ 0, 0, 0, 1], 0.5))

    print(reseni_soustav_lin.gauss_s_pivotováním(np.array([[10, 1, 1],[2, 10, 1],[2, 2, 10]]), np.array([12, 13, 14])))
    print(reseni_soustav_lin.lu_rozklad(np.array([[10, 1, 1],[2, 10, 1],[2, 2, 10]]), np.array([12, 13, 14])))
    print(reseni_soustav_lin.jacobiova(np.array([[10, 1, 1],[2, 10, 1],[2, 2, 10]]), np.array([12, 13, 14])))
    print(reseni_soustav_lin.gauss_seidelova(np.array([[10, 1, 1],[2, 10, 1],[2, 2, 10]]), np.array([12, 13, 14])))
if __name__ == "__main__":
    main()