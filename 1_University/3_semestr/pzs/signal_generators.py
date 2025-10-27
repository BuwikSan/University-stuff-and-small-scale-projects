import matplotlib.pyplot as plt
import numpy as np
from math import pi

def plot_graph(set_of_values):
    plt.grid(True)
    plt.plot(range(len(set_of_values)), set_of_values)
    plt.xlabel("time")
    plt.ylabel("value")
    plt.legend(shadow=True)
    plt.show()

def generate_sin_signal_func(vlnova_delka, faze, am, t):
    y = am * np.sin((2 * pi * t - faze)/vlnova_delka)
    return y

def generate_square_signal_func(vlnova_delka, faze, am, strida, t):
    if (t - faze) % vlnova_delka < strida:
        y = am
    else:
        y = -am
    return y

def generate_triangle_signal_func(vlnova_delka, faze, am, t):
    y = (2 * am) / pi * np.arcsin(np.sin((2 * pi * t - faze)/vlnova_delka))
    return y

def generate_sawtooth_signal_func(vlnova_delka, faze, am, t):
    y = (2 * am) / pi * np.arctan(np.tan((2 * pi * t - faze)/vlnova_delka))
    return y

def generate_impulse_siganl_func():
    ... #TODO

generate_sin_signal = np.vectorize(generate_sin_signal_func)
generate_square_signal = np.vectorize(generate_square_signal_func)
generate_triangle_signal = np.vectorize(generate_triangle_signal_func)
generate_sawtooth_signal = np.vectorize(generate_sawtooth_signal_func)
# generate_impulse_siganl = np.vectorize(generate_impulse_signal_func)

def main():
    casovy_usek = 10
    presnost = 1000
    current_linspace = np.linspace(0, casovy_usek, presnost)


    test_sin_signal = generate_sin_signal(1, 0, 1, current_linspace)
    test_square_signal = generate_square_signal(1, 0, 1, 0.5, current_linspace)
    test_triangle_signal = generate_triangle_signal(1, 0, 1, current_linspace)
    test_sawtooth_signal = generate_sawtooth_signal(1, 0, 1, current_linspace)
    #test_impulse_signal = generate_sin_signal(6, 2, 1, current_linspace)

    plot_graph(test_sin_signal, current_linspace)
    plot_graph(test_square_signal, current_linspace)
    plot_graph(test_triangle_signal, current_linspace)
    plot_graph(test_sawtooth_signal, current_linspace)

if __name__ == "__main__":
    main()


## vlastnosi signálu energie (integrace)
## trend (aproximace)
## výkon (práce za čas)

## naštuduj konvoluci a kovarianci a směrodatnou odchylku 
## a rozptyl a kovariační koeficient a obecně statistiku dodělej 
## a časové řady a 