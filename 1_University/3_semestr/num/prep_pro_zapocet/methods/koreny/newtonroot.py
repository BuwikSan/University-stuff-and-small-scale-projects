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