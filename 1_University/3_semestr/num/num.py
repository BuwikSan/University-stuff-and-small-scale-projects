import numpy as np

class Aproximace_korenu():
    def __init__(self):
        pass
    
    # def newton1(self, f, fd, x0, iter=1000):
    #     for i in range(iter):
    #         x = x0-f(x0)/fd(x0)
    #         x0 = x
    #     return x
    
    # def newton2(self, f, fd, x0, eps=0.00000000001):
    #     while abs(x-x0) > eps:
    #         x = x0-f(x0)/fd(x0)
    #         x0 = x
    #     return x

    def newton(self, f, fd, x0, eps=0.0000000001, iter=1000):
        iterace = 0
        print("Počáteční hodnota:", x0)
        while iterace < iter:
            x = x0 - f(x0)/fd(x0)
            if abs(x - x0) < eps:
                return x
            x0 = x
            iterace += 1

        if iterace == iter:
            raise Exception("Nekonverguje v rozumném počtu iterací")
        else:
            return x
        

    def bisekce(self, f, a, b, eps=0.0000000001, iter=1000):
        if f(a)*f(b) > 0:
            raise Exception("Funkce nemá v intervalu kořen")
        
        iterace = 0
        while abs(b-a) > eps and iterace < iter:
            c = (a+b)/2
            if f(c) == 0:
                return c
            elif f(a)*f(c) < 0:
                b = c
            else:
                a = c
            iterace += 1
        
        if iterace == iter:
            raise Exception("Nekonverguje v rozumném počtu iterací")
        else:
            return (a+b)/2

class reseni_soustav_lin_rovnic:
    def __init__(self):
        pass

    def gauss_s_pivotováním(self, matice_A, vektor_řešení):
        Ab = np.column_stack((matice_A.astype(float), vektor_řešení.astype(float)))
        N = len(matice_A)
        print(Ab)
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
                    print(Ab[j, k] - u * Ab[i, k], Ab[j, k], Ab[i, k])
                    Ab[j, k] = Ab[j, k] + u * Ab[i, k]
                    print(Ab)

        # zpětný chod
        x = np.zeros(N)
        x[N-1] = Ab[N-1, N]/Ab[N-1, N-1]
        for k in range(N-2, -1, -1):
            x[k] = (Ab[k, N] - sum(Ab[k, j] * x[j] for j in range(k+1, N))) / Ab[k, k]
        return x

    def jacobiova(self, matice_A, vektor_řešení):
        N = len(matice_A)
        x = np.zeros(N)
        for it in range(100000):  # max počet iterací
            x_new = np.copy(x)
            for i in range(N):
                s = sum(matice_A[i, j] * x[j] for j in range(N) if j != i)
                x_new[i] = (vektor_řešení[i] - s) / matice_A[i, i]
            x = x_new
        return x

    def gauss_seidelova(self, matice_A, vektor_řešení):
        N = len(matice_A)
        x = np.zeros(N)
        for it in range(100000):  # max počet iterací
            for i in range(N):
                s = sum(matice_A[i, j] * x[j] for j in range(N) if j != i)
                x[i] = (vektor_řešení[i] - s) / matice_A[i, i]
        return x

class lin_interpolace:
    def __init__(self):
        pass

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
    print(aproximator_korenu.newton(lambda x: x*x*x, lambda x: 3*x*x, 8))
    print(aproximator_korenu.bisekce(lambda x: x*x*x, -2, 8))
    print(reseni_soustav_lin.gauss_s_pivotováním(np.array([[2,1,-1],[ -3,-1,2],[ -2,1,2]]), np.array([8,-11,-3])))
    print(reseni_soustav_lin.jacobiova(np.array([[2,1,-1],[ -3,-1,2],[ -2,1,2]]), np.array([8,-11,-3])))
    print(reseni_soustav_lin.gauss_seidelova(np.array([[2,1,-1],[ -3,-1,2],[ -2,1,2]]), np.array([8,-11,-3])))
if __name__ == "__main__":
    main()