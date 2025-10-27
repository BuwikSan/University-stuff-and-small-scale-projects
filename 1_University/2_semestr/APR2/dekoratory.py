def co_se_deje(func):
    def nahradni_funkce(x):
        print(f"Voláme {func.__name__}({x})")
        return func(x)

    return nahradni_funkce

@co_se_deje
def fib(x):
    """Spočítá x-té číslo ve Fibonacciho posloupnosti."""
    if x <= 1:
        return x
    return fib(x - 1) + fib(x - 2)

if __name__ == "__main__":
    print(fib(4))