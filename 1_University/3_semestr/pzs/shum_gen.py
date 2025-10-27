import numpy as np
import matplotlib.pyplot as plt
from scipy import signal


### šum
def zasumuj_signal(signal, mira_rozbiti): #aditivní šum
    return signal + (mira_rozbiti * np.random.randn(len(signal)))

def main(): ## nagenerování signálu a na něj šum (není moje)
    # -----------------------------
    # Parametry signálu
    # -----------------------------
    numT = 6          # počet period
    f = 2             # frekvence [Hz]
    n_length = numT * 100
    tvec = np.linspace(0, numT/f, n_length)

    # -----------------------------
    # Čtvercový signál
    # -----------------------------
    signal_clean = signal.square(2 * np.pi * f * tvec)

    # -----------------------------
    # Přidání malého šumu (poskvrnění)
    # -----------------------------
    noise_amp = 0.2  # nastavení intenzity "rozbití"
    signal_noisy = signal_clean + noise_amp * np.random.randn(n_length)


    N = 20
    kernel = np.ones(N) / N

    # Aplikace konvoluce
    filtered = np.convolve(signal_noisy, kernel, mode='same')

    plt.figure(figsize=(10, 4))
    plt.plot(tvec, signal_noisy, label='poskvrnen', color='red')
    plt.plot(tvec, filtered, label='Původní čtverec', color = 'blue')
    plt.plot(tvec, signal_clean, label='Původní čtverec', color = 'green')
    plt.xlabel('Čas [s]')
    plt.ylabel('Amplituda')
    plt.title('Čtvercový signál rozbitý šumem')
    plt.legend()
    plt.grid(True)
    plt.show()

if __name__ == "__main__":
    main()