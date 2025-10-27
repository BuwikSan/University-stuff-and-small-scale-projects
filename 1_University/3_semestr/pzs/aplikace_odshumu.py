import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from matplotlib.patches import Rectangle
import signal_generators as sigg
from itertools import combinations
from shum_gen import zasumuj_signal
import signal_generators as sg
from cccc import normalized_crosscorr

## techniky na amplifikaci signálu v šumu 
## (musim znát periodu (aspoň přibližně) a pak je to ez)
## perioda jse dobře odhadnout autokorelací

## svatá trojice: konvoluce -> korelace, kovariance (díky nim dokážu poznat povahu signálu)

### ŠUM
## porucha přístroje
## zdroje el napětí / vibrace
## biologické zdroje (dýchání, pohyb)
##
## typy:
## vysokofrekvenční, nízkofrekvenční, pepř a sůl, aditivní
##
## kumulační techniky posílení signálu
## hlavní předpoklady - průměr šumu je nula a konvoluce šumu a signálu je taky nula
## průměrování všech bodů se stejnou souřadnicí vůči periodě
## lze použít i okénkovou kumulaci, nebo exponenciální kumulace


def normalized_autocorr(x, demean=True, unbiased=False):
    x = np.asarray(x, dtype=float).ravel()
    if x.size == 0:
        return np.array([])
    if demean:
        x = x - x.mean()
    corr = np.correlate(x, x, mode='full')  # lags -(N-1)..(N-1)
    if unbiased:
        N = x.size
        lags = np.arange(- (N - 1), N)
        corr = corr / (N - np.abs(lags))
    denom = np.sum(x * x)
    if denom == 0:
        return corr * 0.0
    return corr / denom

def main(): ## nageneruj signal se šumem a pak ho odšumuj (momocí zápisků na začátku) pro aditivní šum
    print("start")

    signal = zasumuj_signal(sg.generate_sin_signal(1, 0, 0.5, np.linspace(0, 500, 100000)), 2)
    sg.plot_graph(signal)
    signal_autocor = normalized_autocorr(signal)[0]
    sg.plot_graph(signal_autocor)

    ## použij kumulační techniky a pak aproximuj 


if __name__ == "__main__":
    main()

# seminární práce zahrnující generaci signálu, konvoluci, korelaci, kovarianci a šum