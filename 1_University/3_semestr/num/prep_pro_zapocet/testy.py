import numpy as np
from math import sin, pi
from scipy.linalg import lu

# lin rovnice ---------------------------------------------------------

def test_gauss_direct(A, b):
    # Profi reference
    x_sure = np.linalg.solve(A, b)
    
    from methods.lin_rovnice.gauss import gauss
    x_mine = gauss(A, b)
    print(f"Gauss Error: {np.linalg.norm(np.array(x_sure) - np.array(x_mine))}")

def test_gauss_pivot(A, b):
    x_sure = np.linalg.solve(A, b)
    
    from methods.lin_rovnice.gausspivot import gauss_pivot
    x_mine = gauss_pivot(A, b)
    print(f"Gauss Pivot Error: {np.linalg.norm(np.array(x_sure) - np.array(x_mine))}")

def test_gauss_seidel(A, b, max_iter=1000, tol=1e-8):
    x_sure = np.linalg.solve(A, b)
    
    from methods.lin_rovnice.gausssiedel import gauss_seidel
    x_mine = gauss_seidel(A, b, max_iter, tol)
    print(f"Gauss-Seidel Error: {np.linalg.norm(np.array(x_sure) - np.array(x_mine))}")

def test_jacobi(A, b, max_iter=1000, tol=1e-8):
    x_sure = np.linalg.solve(A, b)
    
    from methods.lin_rovnice.jacobi import jacobi
    x_mine = jacobi(A, b, max_iter, tol)
    print(f"Jacobi Error: {np.linalg.norm(np.array(x_sure) - np.array(x_mine))}")

def test_gauss_lu(A):
    # Scipy rozklad
    P, L_scipy, U_scipy = lu(A)
    
    from methods.lin_rovnice.gausslu import gauss_lu
    # Tvá funkce vrací matici, kde pod diag je L a na/nad diag je U
    LU_mine = gauss_lu(A)
    print("Gauss-LU dokončen. Porovnej matici LU_mine s L_scipy a U_scipy.")
    print(LU_mine)
    print(L_scipy)
    print(U_scipy)
    print(P)



# kořeny ---------------------------------------------------------------

from scipy.optimize import bisect, newton

def test_bisection(f, a, b):
    root_sure = bisect(f, a, b, xtol=1e-6)
    
    from methods.koreny.bisekce import bisection
    root_mine = bisection(f, a, b, 1e-6, 100)
    print(f"Bisection Error: {abs(root_sure - root_mine)}")

def test_newton_root(f, f_prime, x0):
    # f_prime je derivace pro Newtona (Scipy ji volitelně bere jako fprime)
    root_sure = newton(f, x0, fprime=f_prime)
    
    from methods.koreny.newtonroot import newton as my_newton
    root_mine = my_newton(f, f_prime, x0, 1e-6, 100)
    print(f"Newton Root Error: {abs(root_sure - root_mine)}")




# vyhodnocení polynomů ---------------------------------------------------

from numpy.polynomial.polynomial import polyval

def test_horner(t_points, coefs):
    # polyval bere koefy [a0, a1, a2...] stejně jako tvůj Horner
    val_sure = polyval(t_points, coefs)
    
    from methods.polynomialevaluation.horner import horner
    val_mine = horner(t_points, coefs)
    print(f"Horner Error: {np.linalg.norm(np.array(val_sure) - np.array(val_mine))}")

def test_newton_evaluation(t_points, x_nodes, coefs_diff):
    # Newtonovo vyčíslení nemá v numpy přímý ekvivalent (musel bys převést na standardní tvar)
    # Testuj porovnáním s Lagrangeem nebo jinou interpolací
    from methods.polynomialevaluation.newtoneval import newton_evaluation
    val_mine = newton_evaluation(t_points, x_nodes, coefs_diff)
    print("Newton Eval dokončen.")




# interpolace -----------------------------------------------------------

from scipy.interpolate import lagrange as scipy_lagrange

def test_lagrange(x_points, y_points, t_to_eval):
    poly = scipy_lagrange(x_points, y_points)
    val_sure = poly(t_to_eval)
    
    from methods.interpolace.lagrange import lagrange
    val_mine = lagrange(t_to_eval, x_points, y_points)
    print(f"Lagrange Error: {np.linalg.norm(np.array(val_sure) - np.array(val_mine))}")

def test_vandermonde(x_points, y_points):
    # Vandermonde přes profi řešič koeficientů
    coefs_sure = np.polyfit(x_points, y_points, len(x_points)-1)[::-1]
    
    from methods.interpolace.voldemort import vandermonde
    coefs_mine = vandermonde(x_points, y_points)
    print(f"Vandermonde Coefs Error: {np.linalg.norm(coefs_sure - coefs_mine)}")

def test_newton_interpolation(x_points, y_points):
    from methods.interpolace.newtoninterpolation import newton_interpolation
    coefs_mine = newton_interpolation(x_points, y_points)
    print("Newton Interpolation (Diference) vypočteny.")


# aproximace -----------------------------------------------------------

def test_lsa(x_points, y_points, deg):
    # polyfit vrací [an...a0], otočíme na [a0...an]
    coefs_sure = np.polyfit(x_points, y_points, deg)[::-1]
    
    from methods.aproximace.lsa import lsa
    coefs_mine = lsa(x_points, y_points, deg + 1)
    print(f"LSA Error: {np.linalg.norm(coefs_sure - coefs_mine)}")

def test_lss(A, y):
    x_sure, _, _, _ = np.linalg.lstsq(A, y, rcond=None)
    
    from methods.aproximace.lss import lss
    x_mine = lss(A, y)
    print(f"LSS Error: {np.linalg.norm(x_sure - x_mine)}")

def test_nonlinear_regression(p_data, a_data, am_range, b_range):
    from scipy.optimize import curve_fit
    def model(p, am, b): return (am * b * p) / (1 + b * p)
    
    popt, _ = curve_fit(model, p_data, a_data)
    
    from methods.aproximace.nonlinearregression import nonlinear_fit
    # Rozbalení rozsahů [min, max, step]
    res_mine = nonlinear_fit(p_data, a_data, *am_range, *b_range)
    print(f"Nonlinear Fit Error (vs CurveFit): {np.linalg.norm(popt - res_mine)}")



# integrace -----------------------------------------------------------
from scipy.integrate import simpson, quad, solve_ivp

def test_simpson(f, a, b, n):
    x_vals = np.linspace(a, b, n + 1)
    y_vals = [f(val) for val in x_vals]
    res_sure = simpson(y=y_vals, x=x_vals)
    
    from methods.integral.simpson import simpson_rule
    res_mine = simpson_rule(f, a, b, n)
    print(f"Simpson Error: {abs(res_sure - res_mine)}")

def test_midpoint(f, a, b, n):
    # Quad je nejpřesnější integrace v SciPy
    res_sure, _ = quad(f, a, b)
    
    from methods.integral.midpointrule import midpoint_rule
    res_mine = midpoint_rule(f, a, b, n)
    print(f"Midpoint Error (vs Quad): {abs(res_sure - res_mine)}")



# diferencialní rovnice ---------------------------------------------------

def test_euler_step(f, x0, y0, h, n):
    # Solver pro ODE
    sol = solve_ivp(lambda t, y: f(t, y), [x0, x0 + n*h], [y0], t_eval=np.linspace(x0, x0+n*h, n+1))
    res_sure = sol.y[0]
    
    from methods.dif_rovnice.eulerstep import euler_step
    res_mine = euler_step(f, x0, y0, h, n)
    print(f"Euler Step Error: {np.linalg.norm(res_sure - res_mine)}")



# hlavní testovací skript ---------------------------------------------------

if __name__ == "__main__":
    print("--- START TESTOVÁNÍ NUMERICKÝCH METOD ---\n")

    # 1. Lineární rovnice
    print("[1] Lineární rovnice:")
    A_lin = [[10.0, 2.0, 1.0], [1.0, 15.0, 2.0], [2.0, 3.0, 20.0]]  # Diagonálně dominantní pro Jacobi/Seidel
    b_lin = [13.0, 18.0, 25.0]
    
    test_gauss_direct(A_lin, b_lin)
    test_gauss_pivot(A_lin, b_lin)
    test_gauss_seidel(A_lin, b_lin)
    test_jacobi(A_lin, b_lin)
    test_gauss_lu(A_lin)
    print("-" * 30)

    # 2. Kořeny
    print("[2] Kořeny:")
    f_root = lambda x: x**2 - 2  # Kořen je odmocnina ze 2 (~1.414)
    f_prime = lambda x: 2*x      # Derivace pro Newtona
    
    test_bisection(f_root, 0, 2)
    test_newton_root(f_root, f_prime, 1.5, )
    print("-" * 30)

    # 3. Polynomy (Evaluace a Interpolace)
    print("[3] Polynomy a Interpolace:")
    x_pts = [0.0, 1.0, 2.0]
    y_pts = [1.0, 3.0, 2.0]
    t_eval = [0.5, 1.5]
    coefs_basic = [1.0, 2.0, -0.5] # Polynom 1 + 2x - 0.5x^2

    test_horner(t_eval, coefs_basic)
    test_lagrange(x_pts, y_pts, t_eval)
    test_vandermonde(x_pts, y_pts)
    
    # Pro Newtona nejdřív spočteme diference, pak evaluujeme
    from methods.interpolace.newtoninterpolation import newton_interpolation
    newton_coefs = newton_interpolation(x_pts, y_pts)
    test_newton_evaluation(t_eval, x_pts, newton_coefs)
    print("-" * 30)

    # 4. Aproximace
    print("[4] Aproximace:")
    x_lsa = [0, 1, 2, 3, 4, 5]
    y_lsa = [0.1, 0.9, 2.2, 2.8, 3.9, 5.1] # Skoro přímka y = x
    
    test_lsa(x_lsa, y_lsa, 1) # Lineární regrese (deg=1)
    
    # LSS test (přeurčená soustava)
    A_lss = [[1, 1], [1, 2], [1, 3]]
    y_lss = [1, 2, 2.1]
    test_lss(A_lss, y_lss)
    
    # Nelineární regrese (Langmuir)
    p_data = [1.0, 2.0, 5.0, 10.0, 20.0]
    # Model: am=10, b=0.5 -> a = (10*0.5*p)/(1 + 0.5*p)
    a_data = [(10 * 0.5 * p) / (1 + 0.5 * p) for p in p_data]
    test_nonlinear_regression(p_data, a_data, [8, 12, 0.5], [0.1, 1.0, 0.1])
    print("-" * 30)

    # 5. Integrace a ODE
    print("[5] Integrace a ODE:")
    f_int = lambda x: sin(x)
    
    test_simpson(f_int, 0, pi, 10)
    test_midpoint(f_int, 0, pi, 100)
    
    # ODE: y' = y, y(0) = 1 -> řešení je e^x
    f_ode = lambda x, y: y
    test_euler_step(f_ode, 0.0, 1.0, 0.1, 10)
    
    print("\n--- TESTOVÁNÍ DOKONČENO ---")