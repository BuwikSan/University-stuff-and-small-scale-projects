# AM a FM modulation (plně zvektorizuj) (zopakuj si optimalizaci z msw)

# fx = A_0 * sin(omega * t)
# gx = M * sin(fi * t)
# yx = (A_0 + gx) * sin(omega * t)

import matplotlib.pyplot as plt
import numpy as np
from math import pi

class Signal:
    def __init__(self, A_0, omega, t):
        self.A_0 = A_0
        self.omega = omega
        self.t = t
        
    def func_repr(self):
        return self.A_0 * np.sin(self.omega * self.t)
    
    def AM_func_repr(self, modulating_signal):
        return (self.A_0 + modulating_signal) *  np.sin(self.omega * self.t)

    def FM(self, modulating_signal, kf):
        pass #TODO
    def PM(self, modulating_signal, kp):
        pass #TODO

def am_generator_func(A_0, omega, M, fi, t):
    y = (A_0 + (M * np.sin(fi * t))) * np.sin(omega * t)
    return y


t = np.linspace(0, 10, 10000)
A_0 = 1
omega = 2 * pi
M = 10
fi = 20 * pi

signal_a = Signal(A_0, omega, t)
signal_b = Signal(M, fi, t)
#amplitude_modulated_signal_a_by_b_vectorized = np.vectorize(signal_a.AM_func_repr(signal_b.func_repr()))

amplitude_modulation = np.vectorize(am_generator_func)

modulated_signal = amplitude_modulation(A_0=A_0, omega=omega, M=M, fi=fi, t=t)

def plot_graph(set_of_values):
    plt.grid(True)
    plt.plot(set_of_values)
    plt.xlabel("time")
    plt.ylabel("value")
    plt.legend(shadow=True)
    plt.show()

plot_graph(modulated_signal)


#prace: min max integrace a trend AM



def energie_signalu(signal_linspace):
    def uprava(x):
        y = abs(x**2)
        return y
    def step_of_integration(x):
        if y == None:
            y=0
        y+=x
        return y
    uprav = np.vectorize(uprava)
    integrate_signal = np.vectorize(step_of_integration)
    return integrate_signal(uprav(signal_linspace))[-1]

print(energie_signalu(modulated_signal))
