import math
from matplotlib import pyplot as plt

def příklad():
    from methods.dif_rovnice.eulerstep import euler_step
    from methods.interpolace.newtoninterpolation import newton_interpolation
    from methods.obecne_operace import make_linspace


    N_0 = 60
    #funkce derivace
    def allee(t, N):
        r = 0.5
        A = 20
        K = 100
        t = -r*N*(1-(N/A))*(1-(N/K))
        return t

    vysledky_derivace = euler_step(allee, 0, N_0, 0.1, 100)

    plt.plot(make_linspace(0, len(vysledky_derivace)/10, len(vysledky_derivace)), vysledky_derivace )
    plt.show()

    for i in range(len(vysledky_derivace)):
        if vysledky_derivace[i] > 80:
            dva_body = ((i-1, i), (vysledky_derivace[i-1], vysledky_derivace[i]))
            break
    print(dva_body)
    
    t_k_aprox = newton_interpolation(dva_body[0], dva_body[1])
    print(t_k_aprox)

    def linf(x, t_k):
        return t_k[0] + t_k[1]*x 
    
    linf_gen = [linf(i, t_k_aprox) for i in make_linspace(0.7, 1.1, 200000)]
    plt.plot(linf_gen, make_linspace(0.7, 1.1, 200000))
    plt.show()
    
    def najdi_bod_blizko(tol, vector, ceho):
        for i in range(len(vector)):
            if vector[i] > ceho - tol and vector[i] < ceho + tol:
                return i
        else:
            print("tak nic")

    x_plus= najdi_bod_blizko(0.01, linf_gen, 80)

    t_k = float(make_linspace(0.7, 0.85, 200000)[x_plus]) + float(dva_body[0][0])
    print(t_k/10)


    


if __name__ == "__main__":
    příklad()
    