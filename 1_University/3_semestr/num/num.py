import numpy as np

class Aproximace_korenu():
    def __init__(self):
        pass
    
    def newton1(self, f, fd, x0, iter=1000):
        for i in range(iter):
            x = x0-f(x0)/fd(x0)
            x0 = x
        return x
    
    def newton2(self, f, fd, x0, eps=0.00000000001):
        while abs(x-x0) < eps:
            x = x0-f(x0)/fd(x0)
            x0 = x
        return x
    
    def newton3(self, f, fd, x0, eps =0.0000001, iter=1000):
        iterace = 0
        while abs(x-x0) < eps and iterace < iter:
            x = x0-f(x0)/fd(x0)
            x0 = x
            iterace += 1
        
        if iterace == iter:
            raise Exception("Nekonverguje v rozumném počtu iterací")
        else:
            return x
        
class reseni_rovnic_o_n_neznamych:
    def __init__(self):
        pass
    
    def gauss(matice_A, vektor_řešení): #TODO maš tu indexaci od 1 bacha
        Ab = np.matrix #= #v rku Ab <- cbind(A, b) asi rozšířená matice 
        for i in range(len(matice_A)): #FIXME temp neoptimální
            Ab.append(matice_A[i])
            Ab[i].append(vektor_řešení[i])
        N = len(matice_A)
        # přímý chod
        for i in range(N - 1): 
            u = - q1/Ab[i, i]
            for j in range(i+1, N):
                s = range((i+1), (N + 1))
                Ab[j, s] = Ab[j, s] + Ab[j, i] * u * Ab[i, s]

        # zpětný chod
        x = vektor_řešení
        x[N] = Ab[N, N+1]/Ab[N, N]
        for k in range(N-1, 1):
            pass #TODO snaž se
        return x
    
    def gaussova_s_pivotováním(matice_A, vektor_řešení):
        pass #TODO

    def jacobiova():
        ...
    def gauss_seidelova():
        ...

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
    print("věř mi, něco se stalo")
    print(aproximator_korenu.newton1(lambda x: x*x - 2, lambda x: 2*x, 8))

if __name__ == "__main__":
    main()