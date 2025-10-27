# ## kovarianci

# import numpy as np
# import matplotlib.pyplot as plt
# import pandas as pd
# from matplotlib.patches import Rectangle
# import signal_generators as sigg

# def lin_func(a, b, t):
#     y = a*t + b
#     return y


# generate_lin_signal = np.vectorize(lin_func)

# t = np.linspace(0, 10, 100)

# lin_1 = generate_lin_signal(2, -22, t)
# lin_2 = generate_lin_signal(1.8, 30, t)
# lin_3 = generate_lin_signal(2.1, 11, t)
# lin_4 = generate_lin_signal(3, 2, t)
# sin_signal = sigg.generate_sin_signal(1, 0, 1, t)
# sqare_signal = sigg.generate_square_signal(1, 0, 1, 1, t)
# triangle_signal = sigg.generate_triangle_signal(1, 0, 1, t)
# sawtooth_signal = sigg.generate_sawtooth_signal(1, 0, 1, t)

# signals = np.stack([lin_1, lin_2, lin_3, lin_4])  # shape (4, N)¨
# print(signals)
# covar = np.cov(signals, rowvar=True)  # každý řádek = proměnná

# # hezký výpis jako tabulka (pandas)
# labels = [f"lin_{i+1}" for i in range(signals.shape[0])]
# df = pd.DataFrame(covar, index=labels, columns=labels)
# print("Covariance matrix:")
# print(df.round(4))

# # vykreslení heatmapy + zvýraznění diagonály
# fig, ax = plt.subplots(figsize=(6, 5))
# im = ax.imshow(covar, cmap="viridis", origin="upper", interpolation="nearest")
# ax.set_xticks(np.arange(len(labels)))
# ax.set_yticks(np.arange(len(labels)))
# ax.set_xticklabels(labels)
# ax.set_yticklabels(labels)
# plt.setp(ax.get_xticklabels(), rotation=45, ha="right")

# # obdélníky přes diagonálu (jiná barva / průhlednost)
# for i in range(len(labels)):
#     rect = Rectangle((i - 0.5, i - 0.5), 1, 1, facecolor="red", alpha=0.25, edgecolor="red", linewidth=1)
#     ax.add_patch(rect)

# cbar = fig.colorbar(im, ax=ax)
# cbar.set_label("Covariance")

# ax.set_title("Covariance matrix (diagonal highlighted)")
# plt.tight_layout()
# plt.show()

# # konvoluce


# # korelace a autokorelace (škálování výstupu atd)

# corel = np.correlate(lin_1, lin_3)
# print(corel)

## konvoluce -
## kovariance (popsání lineární závislosti (trendu) dvou časových řad)
## korelace (jak moc slolu souvisí dvě řady na základě průběhu)
## autokorelace
## škálování výstupu atd)



import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from matplotlib.patches import Rectangle
import signal_generators as sigg
from itertools import combinations

def lin_func(a, b, t):
    return a * t + b

def normalized_crosscorr(a, b):
    # odcentrovat a normalizovat, vrací korelaci pro všechny lags (dlouhá forma)
    a = np.asarray(a) - np.mean(a)
    b = np.asarray(b) - np.mean(b)
    raw = np.correlate(a, b, mode="full")
    norm = np.std(a) * np.std(b) * len(a)
    return raw / norm



def main():

    # časová osa
    t = np.linspace(0, 10, 100)

    # signály (přizpůsobit volání podle tvého signal_generators)
    lin_1 = lin_func(2, -22, t)
    lin_2 = lin_func(1.8, 30, t)
    lin_3 = lin_func(2.1, 11, t)
    lin_4 = lin_func(3, 2, t)

    # sin/square/triangle/saw — předpoklad: funkce přijímají (amp, phase, freq, t)
    sin_signal = sigg.generate_sin_signal(1, 0, 1, t)
    square_signal = sigg.generate_square_signal(1, 0, 1, 1, t)
    triangle_signal = sigg.generate_triangle_signal(1, 0, 1, t)
    sawtooth_signal = sigg.generate_sawtooth_signal(1, 0, 1, t)

    # vyber 4 signály, které chceš analyzovat (uprav pořadí / výběr)
    signals = np.stack([sin_signal, square_signal, triangle_signal, sawtooth_signal])  # shape (4, N)
    labels = ["sin", "square", "triangle", "sawtooth"]

    # ----- Pearson correlation matrix -----
    corr = np.corrcoef(signals, rowvar=True)  # každý řádek = proměnná
    df_corr = pd.DataFrame(corr, index=labels, columns=labels)
    print("Pearson correlation matrix:")
    print(df_corr.round(4))

    # heatmap s anotacemi + zvýrazněná diagonála
    fig, ax = plt.subplots(figsize=(6, 5))
    im = ax.imshow(corr, cmap="coolwarm", vmin=-1, vmax=1, origin="upper", interpolation="nearest")
    ax.set_xticks(np.arange(len(labels)))
    ax.set_yticks(np.arange(len(labels)))
    ax.set_xticklabels(labels)
    ax.set_yticklabels(labels)
    plt.setp(ax.get_xticklabels(), rotation=45, ha="right")
    # anotace hodnot
    for i in range(len(labels)):
        for j in range(len(labels)):
            ax.text(j, i, f"{corr[i, j]:.2f}", ha="center", va="center", color="black", fontsize=9)

    # zvýraznění diagonály (jiná barva průhledný pruh)
    for i in range(len(labels)):
        rect = Rectangle((i - 0.5, i - 0.5), 1, 1, facecolor="yellow", alpha=0.25, edgecolor="orange", linewidth=1)
        ax.add_patch(rect)

    cbar = fig.colorbar(im, ax=ax)
    cbar.set_label("Pearson correlation")
    ax.set_title("Correlation matrix (diagonal highlighted)")
    plt.tight_layout()
    plt.savefig("correlation_heatmap.png", dpi=150)
    plt.show()

    # ----- Cross-correlation (normalized) pro všechny párů ----
    N = signals.shape[1]
    lags = np.arange(-N + 1, N)

    pairs = list(combinations(range(len(labels)), 2))
    n_pairs = len(pairs)
    cols = 2
    rows = (n_pairs + cols - 1) // cols
    fig, axes = plt.subplots(rows, cols, figsize=(10, 4 * rows), squeeze=False)
    for idx, (i, j) in enumerate(pairs):
        ax = axes[idx // cols][idx % cols]
        cc = normalized_crosscorr(signals[i], signals[j])
        ax.plot(lags, cc, color="tab:blue")
        ax.axvline(0, color="k", linestyle="--", linewidth=0.6)
        ax.set_title(f"Cross-corr: {labels[i]} vs {labels[j]}")
        ax.set_xlabel("Lag")
        ax.set_ylabel("Normalized cross-correlation")
        ax.grid(alpha=0.2)
    plt.tight_layout()
    plt.savefig("crosscorrelations_pairs.png", dpi=150)
    plt.show()

    # ----- Autocorrelations (for each signal) -----
    fig, axes = plt.subplots(2, 2, figsize=(10, 8))
    for idx in range(len(labels)):
        ax = axes[idx // 2][idx % 2]
        ac = normalized_crosscorr(signals[idx], signals[idx])
        ax.plot(lags, ac, color="tab:green")
        ax.set_title(f"Autocorr: {labels[idx]}")
        ax.set_xlabel("Lag")
        ax.set_xlim(-len(t)//2, len(t)//2)
        ax.grid(alpha=0.2)
    plt.tight_layout()
    plt.savefig("autocorrelations.png", dpi=150)
    plt.show()

if __name__ == "__main__":
    main()