import numpy as np
import matplotlib.pyplot as plt

# Funkce f(x) = x^3 - x - 2, chceme f(x) = 0
# Převod na x = g(x): x = (2 + x) ** (1/3)
def g(x):
    return  (2 + x)**(1/3)

# Fixed point iteration
def fixed_point(g, x0, tol=1e-6, max_iter=50):
    xs = [x0]
    for i in range(max_iter):
        x1 = g(xs[-1])
        xs.append(x1)
        if abs(x1 - xs[-2]) < tol:
            break
    return xs

# Počáteční odhad
x0 = 1.5
iterace = fixed_point(g, x0)

# Grafické znázornění
x = np.linspace(1, 2, 100)
plt.plot(x, g(x), label='g(x)')
plt.plot(x, x, 'k--', label='y=x')
plt.scatter(iterace, [g(xi) for xi in iterace], color='red')
for i in range(len(iterace)-1):
    plt.plot([iterace[i], iterace[i]], [iterace[i], g(iterace[i])], 'r:')
    plt.plot([iterace[i], iterace[i+1]], [g(iterace[i]), g(iterace[i+1])], 'r:')

plt.xlabel('x')
plt.ylabel('y')
plt.legend()
plt.title('Fixed Point Iteration')
plt.show()