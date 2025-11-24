# jsem cooked, neumim to souč se ft a fs
# diskrétní fourierova transformace
# k= 0   S'_0    = S_0*e^(i*0*0)      + S_1*e^(i*0*1)     + S_2*e^(i*0*2)     + ... + S_N*e^(i*0*(N-1))
# k= 1   S'_1    = S_0*e^(i*1*0)      + S_1*e^(i*1*1)     + S_2*e^(i*1*2)     + ... + S_N*e^(i*1*(N-1))
# k= 2   S'_2    = S_0*e^(i*2*0)      + S_1*e^(i*2*1)     + S_2*e^(i*2*2)     + ... + S_N*e^(i*2*(N-1))
# .
# .
# .
# k= N-1 S'_(N-1) = S_0*e^(i*(N-1)*0) + S_1*e^(i*(N-1)*1) + S_2*e^(i*(N-1)*2) + ... + S_N*e^(i*(N-1)*(N-1))
# W = e^(i*2*pi/N)


# ( S_0 + S_1 + S_2 + ... + S_N ) = [[S_0 + S_1*W^0 + S_2*W^0 + ... + S_N*W^0],
#                                    [S_0 + S_1*W^1 + S_2*W^2 + ... + S_N*W^(N-1)], 
#                                    [S_0 + S_1*W^2 + S_2*W^4 + ... + S_N*W^(2(N-1))],
#                                    ...
#                                    [S_0 + S_1*W^(N-1) + S_2*W^2(N-1) + ... + S_N*W^((N-1)*(N-1))]]

# rychlá fourerova transformace

# S(t) = 5 + 2cos(2*pi*t - 90°) + 3cos(4*pi*t)
# f_v = 4 Hz, T = 1/4
# t = {0, T, 2T, 3T} = {0, 1/4, 1/2, 3/4}
# S(0) = 5 + 2cos(0 - 90°) + 3cos(0) = 5 + 3 = 8
# S(T) = 4
# S(2T) = 8 
# S(3T) = 0

# S'_0 = 8 + 4 + 8 + 0 = 20
# S'_1 = 8 + 4W + 8W^2 + 0W^3 = -4i
# S'_2 = 8 + 4W^2 + 8W^4 + 0W^6 = 12
# S'_3 = 8 + 4W^3 + 8W^6 + 0W^9 = 4i

# S'_k = {20, 4, 12, 4}
# názorný graf XD : představivost
#

import time
import numpy as np
import matplotlib.pyplot as plt

def dft(x):
    """
    Vypočítá Diskrétní Fourierovu Transformaci (DFT) 1D signálu x.
    
    Args:
        x (array_like): Vstupní signál (vzorky).
        
    Returns:
        numpy.ndarray: Koeficienty DFT.
    """
    N = len(x)
    X = np.zeros(N, dtype=complex)
    
    # Klasická implementace podle sumačního vzorce
    # X_k = sum_{n=0}^{N-1} x_n * e^(-i * 2*pi * k * n / N)
    for k in range(N):
        sum_val = 0
        for n in range(N):
            W = -1j * 2 * np.pi * k * n / N
            sum_val += x[n] * np.exp(W)
        X[k] = sum_val
        
    return X

# Parametry vzorkování
Fs = 100.0 # Vzorkovací frekvence (Hz)
T = 2.0    # Délka trvání signálu (s)
N = int(Fs * T) # Počet vzorků
t = np.linspace(0, T, N, endpoint=False) # Časový vektor
t2 = np.linspace(0, T*10, N*10, endpoint=False) # časový vektor 2
# Definice signálu: 5 + 2cos(2pi*t - pi/2) + 3cos(4pi*t)
# Poznámka: cos(2pi*t - pi/2) je to samé jako sin(2pi*t)
x = 5 + 2 * np.cos(2 * np.pi * t - np.pi / 2) + 3 * np.cos(4 * np.pi * t)
x2 = 5 + 2 * np.cos(2 * np.pi * t2 - np.pi / 2) + 3 * np.cos(4 * np.pi * t2)

# Výpočet DFT
tic = time.time()
X = dft(x)
tac = time.time()
print("DFT: ", tac - tic)

tic = time.time()
X2 = dft(x2)
tac = time.time()
print("DFT2: ", tac - tic)




# Výpočet frekvenční osy
freqs = np.fft.fftfreq(N, 1/Fs)

# Pro zobrazení bereme jen první polovinu (pozitivní frekvence)
half_N = N // 2
freqs_half = freqs[:half_N]
# Normalizace amplitudy: dělením N získáme skutečné amplitudy sinusovek (pro DC je to N, pro ostatní N/2)
magnitude = np.abs(X[:half_N]) * 2 / N
magnitude[0] = magnitude[0] / 2 # Korekce pro DC složku
# Vykreslení
plt.figure(figsize=(12, 6))
# Časová oblast
plt.subplot(2, 1, 1)
plt.plot(t, x)
plt.title('Vstupní signál: $5 + 2\cos(2\pi t - \pi/2) + 3\cos(4\pi t)$')
plt.xlabel('Čas [s]')
plt.ylabel('Amplituda')
plt.grid(True)
# Frekvenční oblast
plt.subplot(2, 1, 2)
plt.stem(freqs_half, magnitude)
plt.title('Amplitudové spektrum (DFT)')
plt.xlabel('Frekvence [Hz]')
plt.ylabel('Amplituda')
plt.xlim(-0.5, 10) # Omezíme osu X pro lepší viditelnost nízkých frekvencí
plt.grid(True)
plt.tight_layout()
plt.show()