# Pravdepodobnost a statistika – Cvičení 2 (Policie)
# ---------------------------------------------------
# Soubor: policie.csv (náhrada za Policie.RData)
# Vyžaduje: pandas, numpy, matplotlib, scipy

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy import stats

# ---------------------------------------------------
# 1. Načtení dat
# ---------------------------------------------------
policie = pd.read_csv("policie.csv", encoding="utf-8")

# Pomocné funkce
def freq_table(series, bins=None):
    """Vrací DataFrame s četnostmi (n, N, f, F)."""
    if bins is not None:
        counts, edges = np.histogram(series.dropna(), bins=bins)
        labels = [f"({edges[i]:.0f}, {edges[i+1]:.0f}]" for i in range(len(edges)-1)]
        ac = pd.Series(counts, index=labels)
    else:
        ac = series.value_counts().sort_index()
    kac = ac.cumsum()
    rc = (ac / ac.sum()).round(2)
    krc = rc.cumsum().round(2)
    return pd.DataFrame({"n(i)": ac, "N(i)": kac, "f(i)": rc, "F(i)": krc})

def freq_polygon(x, y, title, color="darkblue"):
    plt.figure(figsize=(7,4))
    plt.vlines(x, ymin=0, ymax=y, color=color, linewidth=2)
    plt.plot(x, y, color="royalblue")
    plt.title(title)
    plt.xlabel("Hodnota")
    plt.ylabel("Počet")
    plt.tight_layout()
    plt.show()

# ---------------------------------------------------
# 2. Frekvenční rozdělení – diastolický tlak
# ---------------------------------------------------
diast = pd.to_numeric(policie["diast"], errors="coerce").dropna()

ac = diast.value_counts().sort_index()
kac = ac.cumsum()
rc = (ac / ac.sum()).round(2)
krc = rc.cumsum().round(2)
freq_diast = pd.DataFrame({"n(i)": ac, "N(i)": kac, "f(i)": rc, "F(i)": krc})
print("Diastolický tlak – frekvenční rozdělení:\n")
print(freq_diast, "\n")

# Frekvenční polygon
x = ac.index.to_numpy()
y = ac.values
freq_polygon(x, y, "Frekvenční polygon – diastolický tlak")

# ---------------------------------------------------
# 3. Výška – histogram + frekvenční rozdělení
# ---------------------------------------------------
vyska = pd.to_numeric(policie["height"], errors="coerce").dropna()

plt.figure(figsize=(7,4))
plt.hist(vyska, color="salmon", edgecolor="darkred", bins="auto")
plt.xlabel("Výška (cm)")
plt.title("Histogram výšky")
plt.tight_layout()
plt.show()

counts, breaks = np.histogram(vyska, bins=10)
labels = [f"({breaks[i]:.0f}, {breaks[i+1]:.0f}]" for i in range(len(breaks)-1)]
ac = pd.Series(counts, index=labels)
kac = ac.cumsum()
rc = (ac / ac.sum()).round(2)
krc = rc.cumsum().round(2)
freq_vyska = pd.DataFrame({"n(i)": ac, "N(i)": kac, "f(i)": rc, "F(i)": krc})
print("Výška – frekvenční rozdělení:\n")
print(freq_vyska, "\n")

# ---------------------------------------------------
# 4. Puls – histogram + frekvenční rozdělení
# ---------------------------------------------------
puls = pd.to_numeric(policie["pulse"], errors="coerce").dropna()

plt.figure(figsize=(7,4))
plt.hist(puls, color="salmon", edgecolor="darkred", bins="auto")
plt.xlabel("Puls")
plt.title("Histogram pulsu")
plt.tight_layout()
plt.show()

counts, breaks = np.histogram(puls, bins=10)
labels = [f"({breaks[i]:.0f}, {breaks[i+1]:.0f}]" for i in range(len(breaks)-1)]
ac = pd.Series(counts, index=labels)
kac = ac.cumsum()
rc = (ac / ac.sum()).round(2)
krc = rc.cumsum().round(2)
freq_puls = pd.DataFrame({"n(i)": ac, "N(i)": kac, "f(i)": rc, "F(i)": krc})
print("Puls – frekvenční rozdělení:\n")
print(freq_puls, "\n")

# ---------------------------------------------------
# 5. Krabicový graf a kvantily – výška
# ---------------------------------------------------
plt.figure(figsize=(5,5))
plt.boxplot(vyska, patch_artist=True,
            boxprops=dict(facecolor="yellow", edgecolor="orange"),
            medianprops=dict(color="black"))
plt.title("Krabicový graf výšky")
plt.ylabel("Výška (cm)")
plt.tight_layout()
plt.show()

# Bez odlehlých
plt.figure(figsize=(5,5))
plt.boxplot(vyska, patch_artist=True, whis=3,
            boxprops=dict(facecolor="yellow", edgecolor="orange"),
            medianprops=dict(color="black"), showfliers=False)
plt.title("Krabicový graf výšky (bez odlehlých pozorování)")
plt.ylabel("Výška (cm)")
plt.tight_layout()
plt.show()

# Kvantily / percentily
print("Výška – popisné statistiky polohy:\n")
print("min:", vyska.min())
print("max:", vyska.max())
print("Q1:", vyska.quantile(0.25))
print("Q3:", vyska.quantile(0.75))
print("median:", vyska.median())
print("five-number summary:", [vyska.min(), vyska.quantile(0.25), vyska.median(), vyska.quantile(0.75), vyska.max()])
print("mean:", vyska.mean())
print("summary():\n", vyska.describe(), "\n")

# ---------------------------------------------------
# 6. Hmotnost – histogram a průměr odhadem
# ---------------------------------------------------
vaha = pd.to_numeric(policie["weight"], errors="coerce").dropna()

plt.figure(figsize=(7,4))
plt.hist(vaha, color="salmon", edgecolor="darkred", bins="auto")
plt.xlabel("Váha (kg)")
plt.title("Histogram váhy")
plt.tight_layout()
plt.show()

counts, mids = np.histogram(vaha, bins=10)
midpoints = 0.5 * (mids[1:] + mids[:-1])
weighted_mean = np.average(midpoints, weights=counts)
print("Váha – vážený průměr (odhad z histogramu):", round(weighted_mean, 2))
print("summary():\n", vaha.describe(), "\n")

# ---------------------------------------------------
# 7. Tuk (%) – histogram + popisné statistiky
# ---------------------------------------------------
tuk = pd.to_numeric(policie["fat"], errors="coerce").dropna()

plt.figure(figsize=(7,4))
plt.hist(tuk, color="salmon", edgecolor="darkred", bins="auto")
plt.xlabel("Tuk (%)")
plt.title("Histogram tuku")
plt.tight_layout()
plt.show()

print("Tuk – popisné statistiky polohy:\n", tuk.describe(), "\n")

# ---------------------------------------------------
# 8. Variabilita – výška
# ---------------------------------------------------
print("Výška – popisné statistiky variability:\n")
print("Rozptyl:", vyska.var())
print("Směr. odchylka:", vyska.std())
print("IQR:", vyska.quantile(0.75) - vyska.quantile(0.25))
print("MAD:", stats.median_abs_deviation(vyska))
print("Variabilita (koef. variace):", vyska.std() / vyska.mean())

# ---------------------------------------------------
# 9. Variabilita – váha
# ---------------------------------------------------
print("\nVáha – popisné statistiky variability:\n")
print("Rozptyl:", vaha.var())
print("Směr. odchylka:", vaha.std())
print("Koef. variace:", vaha.std() / vaha.mean())

# ---------------------------------------------------
# 10. Tvar rozdělení – výška
# ---------------------------------------------------
z_vyska = stats.zscore(vyska, nan_policy="omit")
print("\nZ-skóry – výška (ukázka):", z_vyska[:5])
print("Šikmost (skewness):", stats.skew(vyska, nan_policy="omit"))
print("Špičatost (kurtosis):", stats.kurtosis(vyska, nan_policy="omit"))

# ---------------------------------------------------
# 11. Tuk – tvar rozdělení
# ---------------------------------------------------
print("\nTuk – tvar rozdělení:\n")
print("Šikmost:", stats.skew(tuk, nan_policy='omit'))
print("Špičatost:", stats.kurtosis(tuk, nan_policy='omit'))

# ---------------------------------------------------
# 12. Reakční doba – histogram + boxplot
# ---------------------------------------------------
doba = pd.to_numeric(policie["react"], errors="coerce").dropna()

plt.figure(figsize=(7,4))
plt.hist(doba, color="lightblue", edgecolor="darkblue", bins="auto")
plt.xlabel("Reakční doba")
plt.title("Histogram reakční doby")
plt.tight_layout()
plt.show()

plt.figure(figsize=(5,5))
plt.boxplot(doba, patch_artist=True,
            boxprops=dict(facecolor="lightyellow", edgecolor="orange"),
            medianprops=dict(color="black"))
plt.title("Krabicový graf reakční doby")
plt.ylabel("Reakční doba")
plt.tight_layout()
plt.show()

# ---------------------------------------------------
# 13. Posun a změna měřítka (výška)
# ---------------------------------------------------
vyska_p = vyska + 10
vyska_m = vyska * 10

summary_shift = pd.DataFrame({
    "Průměr": [vyska.mean(), vyska_p.mean(), vyska_m.mean()],
    "Sm. odch.": [vyska.std(), vyska_p.std(), vyska_m.std()],
    "Šikmost": [stats.skew(vyska), stats.skew(vyska_p), stats.skew(vyska_m)],
    "Špičatost": [stats.kurtosis(vyska), stats.kurtosis(vyska_p), stats.kurtosis(vyska_m)]
}, index=["vyska", "vyska+10", "vyska*10"])

print("\nVliv posunu a změny měřítka na statistiky:\n")
print(summary_shift, "\n")

fig, axes = plt.subplots(1, 3, figsize=(12, 4))
axes[0].hist(vyska, color="lightgreen")
axes[1].hist(vyska_p, color="lightgreen")
axes[2].hist(vyska_m, color="lightgreen")
axes[0].set_title("Výška")
axes[1].set_title("Výška + 10")
axes[2].set_title("Výška * 10")
plt.tight_layout()
plt.show()
