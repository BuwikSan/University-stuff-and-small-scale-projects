# Cvičení 2 — Pravděpodobnost a statistika (kompletní přepis a opravy)
# --------------------------------------------------------------------
# Vyžaduje: pandas, numpy, matplotlib
# Soubory:  duvera.csv  (náhrada za Duvera_24.RData)
#           Cars93.csv  (náhrada za MASS::Cars93)

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path

# -------------------------------
# Pomocné funkce
# -------------------------------

def freq_table(series, order=None, pct_decimals=2):
    """Vrať DataFrame s absolutními a relativními četnostmi (v %)."""
    s = pd.Series(series).dropna()
    if order is not None:
        counts = s.value_counts().reindex(order, fill_value=0)
    else:
        counts = s.value_counts().sort_index()
    rel = (counts / counts.sum() * 100).round(pct_decimals) if counts.sum() > 0 else counts.astype(float)
    return pd.DataFrame({"absolutni": counts, "relativni (%)": rel})

def bar_with_labels(counts, title, ylabel="Absolutni cetnosti", ylim_pad=2):
    """Sloupcový graf s čísly nad sloupci. (Bez vykreslení, pokud prázdné.)"""
    if len(counts) == 0 or counts.sum() == 0:
        print(f"[SKIP] {title}: prázdné vstupní hodnoty.")
        return
    idx = counts.index.astype(str)
    vals = counts.values
    plt.figure(figsize=(8, 4))
    plt.bar(idx, vals)
    plt.title(title)
    plt.ylabel(ylabel)
    plt.ylim(0, max(vals) + ylim_pad)
    for i, v in enumerate(vals):
        plt.text(i, v + 0.5, str(v), ha="center", va="bottom")
    plt.tight_layout()
    plt.show()

def pie_with_labels(props, title):
    """Koláčový graf s popisky 'název (xx.xx%)'. (Bez vykreslení, pokud prázdné.)"""
    if len(props) == 0 or props.sum() == 0:
        print(f"[SKIP] {title}: prázdné vstupní hodnoty.")
        return
    labels = [f"{lab} ({pct:.2f}%)" for lab, pct in zip(props.index.astype(str), props.values * 100)]
    plt.figure(figsize=(5, 5))
    plt.pie(props.values, labels=labels, startangle=90)
    plt.title(title)
    plt.tight_layout()
    plt.show()

def freq_polygon(x_vals, counts, title, xlab, ylab="Absolutni cetnosti",
                 vline_color="darkgreen", line_color="red"):
    """Frekvenční polygon: svislé čáry + spojnice vrcholů."""
    if len(counts) == 0 or np.nansum(counts) == 0:
        print(f"[SKIP] {title}: prázdné vstupní hodnoty.")
        return
    x = np.array(x_vals, dtype=float)
    y = np.array(counts, dtype=float)
    order = np.argsort(x)
    x, y = x[order], y[order]
    plt.figure(figsize=(7, 4))
    plt.vlines(x, ymin=0, ymax=y, color=vline_color, linewidth=3)
    plt.plot(x, y, color=line_color)
    plt.title(title)
    plt.xlabel(xlab)
    plt.ylabel(ylab)
    plt.tight_layout()
    plt.show()

# -------------------------------
# Načtení dat
# -------------------------------

duvera_path = Path("1_University\\3_semestr\\pas\\python-rewrite\\duvera.csv")
cars_path   = Path("1_University\\3_semestr\\pas\\python-rewrite\\Cars93.csv")

if not duvera_path.exists():
    raise FileNotFoundError("Soubor 'duvera.csv' nebyl nalezen.")
duvera = pd.read_csv(duvera_path, encoding="utf-8")

if cars_path.exists():
    cars = pd.read_csv(cars_path, encoding="utf-8")
else:
    print("[UPOZORNĚNÍ] 'Cars93.csv' nebyl nalezen. Číselná část (Cars93) bude přeskočena.")
    cars = None

# -------------------------------
# Region - NUTS2 (nominální)
# -------------------------------

nuts2_labels = [
    "Praha", "Stredni Cechy", "Jihozapad", "Severozapad",
    "Severovychod", "Jihovychod", "Stredni Morava", "Moravskoslezsko"
]
nuts2_raw = duvera["NUTS2"]

# Pokud jsou hodnoty 1..8 → mapuj na labels. Jinak ponech textové hodnoty.
if pd.to_numeric(nuts2_raw, errors="coerce").dropna().between(1, 8).all():
    nuts2 = pd.to_numeric(nuts2_raw, errors="coerce").map({i+1: lab for i, lab in enumerate(nuts2_labels)})
else:
    nuts2 = nuts2_raw.astype(str).where(nuts2_raw.notna())

print("NUTS2 - unikátní hodnoty:")
print(pd.Series(nuts2).dropna().unique(), "\n")

freq_nuts2 = freq_table(nuts2)
print("Regiony NUTS2 - četnosti:")
print(freq_nuts2, "\n")

# Grafy
counts_nuts2 = pd.Series(nuts2).value_counts().sort_index()
bar_with_labels(counts_nuts2, "Cetnosti regionu CR")
props_nuts2 = (counts_nuts2 / counts_nuts2.sum()) if counts_nuts2.sum() else counts_nuts2.astype(float)
pie_with_labels(props_nuts2, "Relativni cetnosti regionu CR")

# -------------------------------
# Spokojenost se životem (OV_1) - ordinální, opravené mapování
# -------------------------------

ov1_labels = [
    "velmi spokojen", "spíše spokojen", "ani spokojen, ani nespokojen",
    "spíše nespokojen", "velmi nespokojen"
]
ov1_map = {i+1: lab for i, lab in enumerate(ov1_labels)}

ov_1_codes = pd.to_numeric(duvera["OV_1"], errors="coerce")
# Vezmi pouze 1..5, ostatní (0, 8, 9, 99…) → NaN
ov_1 = ov_1_codes.where(ov_1_codes.between(1, 5)).map(ov1_map)
ov_1 = pd.Categorical(ov_1, categories=ov1_labels, ordered=True)

print("OV_1 - unikátní hodnoty:")
print(pd.Series(ov_1).dropna().unique(), "\n")

ac_ov1 = pd.Series(ov_1).value_counts().reindex(ov1_labels, fill_value=0)
if ac_ov1.sum() == 0:
    print("OV_1 - deskriptivní tabulka: žádná validní 1..5 data po očištění.\n")
else:
    kac = ac_ov1.cumsum()
    rc = (ac_ov1 / ac_ov1.sum()).round(2)
    krc = rc.cumsum().round(2)
    tab_ov1 = pd.DataFrame({"n(i)": ac_ov1, "N(i)": kac, "f(i)": rc, "F(i)": krc})
    print("OV_1 - deskriptivní tabulka:")
    print(tab_ov1, "\n")

    bar_with_labels(ac_ov1, "Spokojenost se zivotem")
    pie_with_labels(rc, "Spokojenost se zivotem (relativní)")

# -------------------------------
# Důvěra v média podle pohlaví
# -------------------------------

# pohlaví: 1 -> Muž, 2 -> Žena
pohlavi_codes = pd.to_numeric(duvera.get("IDE_8"), errors="coerce")
pohlavi = pohlavi_codes.map({1: "Muz", 2: "Zena"})

# PI_1z: ponech 1..4, ostatní NaN; mapuj na text
pi_labels = ["rozhodně důvěřuji", "spíše důvěřuji", "spíše nedůvěřuji", "rozhodně nedůvěřuji"]
pi_map = {i+1: lab for i, lab in enumerate(pi_labels)}
pi_codes = pd.to_numeric(duvera.get("PI_1z"), errors="coerce")
pi_clean = pi_codes.where(pi_codes.between(1, 4)).map(pi_map)

tab = pd.crosstab(pohlavi, pi_clean).reindex(columns=pi_labels, fill_value=0).dropna(how="all")
print("Tabulka pohlaví × důvěra v média:")
print(tab, "\n")

if tab.size and tab.to_numpy().sum() > 0:
    row_props = tab.div(tab.sum(axis=1), axis=0).fillna(0).round(3)
    print("Řádkové proporce (podíly v rámci pohlaví):")
    print(row_props, "\n")

    ax = row_props.plot(kind="bar", stacked=True, figsize=(8, 4))
    ax.set_title("Duvera mediim podle pohlavi")
    ax.set_ylabel("Podil")
    ax.legend(title="Důvěra", bbox_to_anchor=(1.02, 1), loc="upper left")
    plt.tight_layout()
    plt.show()
else:
    print("Kontingenční tabulka prázdná - zkontrolujte sloupce IDE_8 a PI_1z.\n")

# -------------------------------
# Číselné proměnné - Cars93 (pokud dataset existuje)
# -------------------------------

if cars is not None:
    # Cylinders včetně 'rotary'
    valce = cars["Cylinders"].astype(str)
    ac_all = valce.value_counts().sort_index()
    print("Cylinders - četnosti (včetně 'rotary'):")
    print(ac_all, "\n")

    # Bez 'rotary'
    valce2 = valce[valce != "rotary"]
    ac = valce2.value_counts().sort_index()
    kac = ac.cumsum()
    rc = (ac / ac.sum()).round(2) if ac.sum() else ac.astype(float)
    krc = rc.cumsum().round(2) if ac.sum() else rc
    tab_valce2 = pd.DataFrame({"n(i)": ac, "N(i)": kac, "f(i)": rc, "F(i)": krc})
    print("Cylinders (bez 'rotary') - frekvenční rozdělení:")
    print(tab_valce2, "\n")

    # Frekvenční polygon pro valce2
    # Pouze hodnoty, které lze převést na číslo:
    x_vals = pd.to_numeric(ac.index, errors="coerce")
    mask = ~x_vals.isna()
    freq_polygon(x_vals[mask], ac.values[mask], "Frekvencni polygon (Cylinders bez 'rotary')", "Pocet valcu")

    # RPM - polygon + histogram
    rpm = pd.to_numeric(cars["RPM"], errors="coerce").dropna()
    ac_rpm = rpm.value_counts().sort_index()
    freq_polygon(ac_rpm.index, ac_rpm.values, "Frekvencni polygon proměnné RPM", "Otáčky motoru (RPM)")

    plt.figure(figsize=(7, 4))
    plt.hist(rpm, bins="auto", color="skyblue", edgecolor="darkblue")
    plt.title("Histogram RPM")
    plt.xlabel("Pocet otacek")
    plt.ylabel("Absolutni cetnosti")
    plt.tight_layout()
    plt.show()

    # Horsepower (hp) - histogramy, frekvenční rozdělení, boxploty, kvantily
    hp = pd.to_numeric(cars["Horsepower"], errors="coerce").dropna()

    plt.figure(figsize=(7, 4))
    plt.hist(hp, bins="auto", color="skyblue", edgecolor="darkblue")
    plt.title("Histogram - Sila vozu (Horsepower)")
    plt.xlabel("Sila vozu")
    plt.ylabel("Absolutni cetnosti")
    plt.tight_layout()
    plt.show()

    plt.figure(figsize=(7, 4))
    plt.hist(hp, bins=10, color="skyblue", edgecolor="darkblue")
    plt.title("Histogram - Sila vozu (Horsepower), breaks = 10")
    plt.xlabel("Sila vozu")
    plt.ylabel("Absolutni cetnosti")
    plt.tight_layout()
    plt.show()

    counts, breaks = np.histogram(hp, bins=10)
    labels = [f"({breaks[i]:.0f}, {breaks[i+1]:.0f}]" for i in range(len(breaks)-1)]
    ac_hp = pd.Series(counts, index=labels)
    kac_hp = ac_hp.cumsum()
    rc_hp = (ac_hp / ac_hp.sum()).round(3) if ac_hp.sum() else ac_hp.astype(float)
    krc_hp = rc_hp.cumsum().round(3) if ac_hp.sum() else rc_hp
    freq_hp = pd.DataFrame({"n(i)": ac_hp, "N(i)": kac_hp, "f(i)": rc_hp, "F(i)": krc_hp})
    print("Horsepower - frekvenční rozdělení podle histogramu (10 tříd):")
    print(freq_hp, "\n")

    # Length - histogram + summary
    length = pd.to_numeric(cars["Length"], errors="coerce").dropna()
    print("Length - summary:")
    print(length.describe(), "\n")

    plt.figure(figsize=(7, 4))
    plt.hist(length, bins=10, color="lightblue", edgecolor="darkblue")
    plt.title("Histogram délky vozu")
    plt.xlabel("Délka vozu (v palcích)")
    plt.ylabel("Absolutni cetnosti")
    plt.tight_layout()
    plt.show()

    # Boxploty pro hp
    plt.figure(figsize=(5, 5))
    plt.boxplot(hp, patch_artist=True,
                boxprops=dict(facecolor="yellow", edgecolor="orange"),
                medianprops=dict(color="black"))
    plt.title("Krabicovy graf - Horsepower (s outliery)")
    plt.ylabel("Sila vozu")
    plt.tight_layout()
    plt.show()

    # Bez odlehlých (whis=3 ~ range=3 v R)
    plt.figure(figsize=(5, 5))
    plt.boxplot(hp, patch_artist=True, whis=3,
                boxprops=dict(facecolor="yellow", edgecolor="orange"),
                medianprops=dict(color="black"), showfliers=False)
    plt.title("Krabicovy graf - Horsepower (bez odlehlých pozorování)")
    plt.ylabel("Sila vozu")
    plt.tight_layout()
    plt.show()

    # Kvantily, pěticíslo, průměr, summary
    print("hp - min:", float(hp.min()))
    print("hp - max:", float(hp.max()))
    print("hp - Q1 (0.25):", float(hp.quantile(0.25)))
    print("hp - Q3 (0.75):", float(hp.quantile(0.75)))
    print("hp - median:", float(hp.median()))
    five_num = [float(hp.min()), float(hp.quantile(0.25)), float(hp.median()),
                float(hp.quantile(0.75)), float(hp.max())]
    print("hp - five-number summary [min, Q1, median, Q3, max]:")
    print(five_num, "\n")
    print("hp - mean:", float(hp.mean()))
    print("hp - summary() ekvivalent:")
    print(hp.describe(), "\n")

    # Další proměnné: Length, Price, Weight
    for var in ["Length", "Price", "Weight"]:
        s = pd.to_numeric(cars[var], errors="coerce").dropna()
        print(f"{var} - summary:")
        print(s.describe(), "\n")

        plt.figure(figsize=(7, 4))
        plt.hist(s, bins=10, color="skyblue", edgecolor="darkblue")
        plt.title(f"Histogram - {var}")
        plt.xlabel(var)
        plt.ylabel("Absolutni cetnosti")
        plt.tight_layout()
        plt.show()

        plt.figure(figsize=(5, 5))
        plt.boxplot(s, patch_artist=True,
                    boxprops=dict(facecolor="khaki", edgecolor="saddlebrown"),
                    medianprops=dict(color="black"))
        plt.title(f"Krabicovy graf - {var}")
        plt.ylabel(var)
        plt.tight_layout()
        plt.show()

    # Porovnání skupin - cena podle původu
    if "Origin" in cars.columns and "Price" in cars.columns:
        puvod = cars["Origin"]
        cena = pd.to_numeric(cars["Price"], errors="coerce")
        grp_summary = cena.groupby(puvod).describe()
        print("Cena podle původu (groupby/summary):")
        print(grp_summary, "\n")
