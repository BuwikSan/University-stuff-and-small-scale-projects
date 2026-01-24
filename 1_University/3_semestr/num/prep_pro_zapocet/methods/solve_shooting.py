"""Solve the boundary/integral-constrained ODE

    y'(x) - y(x) + x = 0,  with constraint  ∫_0^1 y(x) dx = 2

We use only the numerical routines available in the `methods/` folder:
 - Euler solver: methods.dif_rovnice.eulerstep.euler_step
 - Simpson integration: methods.integral.simpson.simpson_rule
 - Root finder (bisection): methods.koreny.bisection.bisection

Approach (shooting): treat y(0)=y0 as parameter, solve ODE over [0,1],
compute I(y0)=∫_0^1 y(x) dx and find y0 such that I(y0)=2 via bisection.

This script is intentionally simple and uses linear interpolation to
provide a callable y(x) for the Simpson integrator.
"""

from methods.dif_rovnice.eulerstep import euler_step
from methods.integral.simpson import simpson_rule
from methods.koreny.bisekce import bisection

def solve_for_y0(y0, x0=0.0, x1=1.0, n_steps=1000, simpson_n=1000):
    """Given initial y(0)=y0, integrate ODE with Euler and return integral ∫_0^1 y - 2.

    We return F(y0) = ∫_0^1 y(x; y0) dx - 2. Root of F is desired y0.
    """
    # ODE: y' = y - x
    f = lambda x, y: y - x

    h = (x1 - x0) / n_steps
    ys = euler_step(f, x0, y0, h, n_steps)  # returns list of n_steps+1 y-values
    xs = [x0 + i * h for i in range(n_steps + 1)]

    # Linear interpolator for y(x) based on xs, ys
    def y_of_x(x):
        if x <= xs[0]:
            return ys[0]
        if x >= xs[-1]:
            return ys[-1]
        # find right interval (simple linear scan; ok for moderate n)
        # For speed you could use bisect from stdlib, but we keep it explicit.
        i = int((x - x0) / h)
        # clamp
        if i < 0: i = 0
        if i >= n_steps: i = n_steps - 1
        xL = xs[i]
        xR = xs[i+1]
        yL = ys[i]
        yR = ys[i+1]
        # linear interp
        t = (x - xL) / (xR - xL)
        return yL + t * (yR - yL)

    # Simpson requires an even number of intervals
    if simpson_n % 2 != 0:
        simpson_n += 1

    integral = simpson_rule(y_of_x, x0, x1, simpson_n)
    return integral - 2.0


def find_initial_y0(bracket=(0.0, 3.0), tol=1e-6, max_iter=60):
    a, b = bracket
    func = lambda y0: solve_for_y0(y0)
    root = bisection(func, a, b, tol, max_iter)
    return root


if __name__ == '__main__':
    print('Running shooting solver (Euler + Simpson + bisection)')
    # coarse settings; increase n_steps/simpson_n for more accuracy
    y0_root = find_initial_y0(bracket=(0.0, 4.0), tol=1e-8, max_iter=80)
    if y0_root is None:
        print('Root finding failed; try different bracket or increase accuracy')
    else:
        print(f'Found initial y(0) = {y0_root}')
        # compute final solution and print approximate integral to verify
        diff = solve_for_y0(y0_root)
        print(f'Check: integral-2 = {diff} (should be ~0)')
