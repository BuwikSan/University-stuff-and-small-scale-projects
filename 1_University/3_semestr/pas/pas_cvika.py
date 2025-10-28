import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import pas_file_handling as pasfh
from pathlib import Path
from scipy import stats
import pas_graph as pasgr

def cvika_1():
        # --- Načtení dat ze souboru prij.csv ---
    prij = pd.read_csv("1_University\\3_semestr\\pas\\python-rewrite\\prij.csv", encoding="utf-8")

    # --- Absolutní a relativní četnosti pro Matur.drive ---
    matur = prij["Matur.drive"]

    # Absolutní četnosti
    abs_counts = matur.value_counts().sort_index()

    # Relativní četnosti (%)
    rel_counts = (abs_counts / abs_counts.sum() * 100).round(2)

    # Kombinovaná tabulka
    freq_matur = pd.DataFrame({
        "absolutni": abs_counts,
        "relativni (%)": rel_counts
    })
    print("Matur.drive - četnosti:")
    print(freq_matur, "\n")


    # --- Absolutní a relativní četnosti pro známky ze statistiky ---
    stat = prij["stat"]

    abs_stat = stat.value_counts().sort_index()
    rel_stat = (abs_stat / abs_stat.sum() * 100).round(2)

    freq_stat = pd.DataFrame({
        "absolutni": abs_stat,
        "relativni (%)": rel_stat
    })
    print("Stat - četnosti:")
    print(freq_stat, "\n")


    # --- Kumulativní četnosti pro uspořádanou kategorickou proměnnou ---
    tab = abs_stat
    cum_abs = tab.cumsum()
    rel = (tab / tab.sum() * 100).round(2)
    cum_rel = rel.cumsum().round(2)

    cum_table = pd.DataFrame({ ## neeeeee cumtable neeeee
        "n(i)": tab,
        "N(i)": cum_abs,
        "p(i) [%]": rel,
        "P(i) [%]": cum_rel
    })
    print("Stat - kumulativní četnosti:")
    print(cum_table)


    # --- Assume 'matur' already exists from the first part ---
    # matur = prij["Matur.drive"]

    # Převod na kategorii pro jistotu
    matur = pd.Series(matur).astype("category")




    # [GRAF] Vstup: counts (četnosti), x_labels, y_values
    counts = matur.value_counts().sort_index()
    # # # # # # # # x_labels = counts.index.astype(str)
    # # # # # # # # y_values = counts.values

    # --- Sloupcový graf ---
    pasgr.bar_with_labels(counts, "Sloupcový graf – Maturita dříve", ylabel="Počet")


    # # # # # # # # plt.figure(figsize=(6, 4))
    # # # # # # # # bars = plt.bar(x_labels, y_values, color=["#66c2a5", "#fc8d62"])
    # # # # # # # # plt.title("Sloupcový graf – Maturita dříve")
    # # # # # # # # plt.xlabel("Kategorie")
    # # # # # # # # plt.ylabel("Počet")

    # # # # # # # # # Popisky nad sloupci
    # # # # # # # # for i, val in enumerate(y_values):
    # # # # # # # #     plt.text(i, val + 0.5, str(val), ha='center', va='bottom')

    # # # # # # # # plt.ylim(0, max(y_values) * 1.2)
    # # # # # # # # plt.tight_layout()
    # # # # # # # # plt.show()


    # --- Koláčový graf s popisky (v procentech) ---
    pasgr.pie_with_labels((counts / counts.sum()) if counts.sum() else counts.astype(float), "Koláčový graf – Maturita dříve")


    # # # # # # # # --- Koláčový graf s popisky (v procentech) ---
    # # # # # # # # [GRAF] Vstup: y_values, labels_with_pct
    # # # # # # # # rel_perc = (counts / counts.sum() * 100).round(2)
    # # # # # # # # labels_with_pct = [f"{lab} ({pct}%)" for lab, pct in zip(x_labels, rel_perc)]

    # # # # # # # # plt.figure(figsize=(5, 5))
    # # # # # # # # plt.pie(
    # # # # # # # #     y_values,
    # # # # # # # #     labels=labels_with_pct,
    # # # # # # # #     colors=["#66c2a5", "#fc8d62"],
    # # # # # # # #     startangle=90,
    # # # # # # # #     autopct=None  # popisky máme ručně
    # # # # # # # # )
    # # # # # # # # plt.title("Koláčový graf s popisky – Maturita dříve")
    # # # # # # # # plt.tight_layout()
    # # # # # # # # plt.show()




    # # # # # # # # --- Koláčový graf bez popisků ---
    # # # # # # # # [GRAF] Vstup: y_values


    # # # # # # # # plt.figure(figsize=(5, 5))
    # # # # # # # # plt.pie(
    # # # # # # # #     y_values,
    # # # # # # # #     colors=["#66c2a5", "#fc8d62"],
    # # # # # # # #     startangle=90,
    # # # # # # # # )
    # # # # # # # # plt.title("Koláčový graf – Maturita dříve")
    # # # # # # # # plt.show()









# def cvika_2():
#     # -------------------------------
#     # Načtení dat
#     # -------------------------------

#     duvera_path = Path("1_University\\3_semestr\\pas\\python-rewrite\\duvera.csv")
#     cars_path   = Path("1_University\\3_semestr\\pas\\python-rewrite\\Cars93.csv")

#     if not duvera_path.exists():
#         raise FileNotFoundError("Soubor 'duvera.csv' nebyl nalezen.")
#     duvera = pd.read_csv(duvera_path, encoding="utf-8")

#     if cars_path.exists():
#         cars = pd.read_csv(cars_path, encoding="utf-8")
#     else:
#         print("[UPOZORNĚNÍ] 'Cars93.csv' nebyl nalezen. Číselná část (Cars93) bude přeskočena.")
#         cars = None

#     # -------------------------------
#     # Region - NUTS2 (nominální)
#     # -------------------------------

#     nuts2_labels = [
#         "Praha", "Stredni Cechy", "Jihozapad", "Severozapad",
#         "Severovychod", "Jihovychod", "Stredni Morava", "Moravskoslezsko"
#     ]
#     nuts2_raw = duvera["NUTS2"]

#     # Pokud jsou hodnoty 1..8 → mapuj na labels. Jinak ponech textové hodnoty.
#     if pd.to_numeric(nuts2_raw, errors="coerce").dropna().between(1, 8).all():
#         nuts2 = pd.to_numeric(nuts2_raw, errors="coerce").map({i+1: lab for i, lab in enumerate(nuts2_labels)})
#     else:
#         nuts2 = nuts2_raw.astype(str).where(nuts2_raw.notna())

#     print("NUTS2 - unikátní hodnoty:")
#     print(pd.Series(nuts2).dropna().unique(), "\n")

#     freq_nuts2 = pasgr.freq_table(nuts2)
#     print("Regiony NUTS2 - četnosti:")
#     print(freq_nuts2, "\n")




#     # Grafy
#     counts_nuts2 = pd.Series(nuts2).value_counts().sort_index()
#     pasgr.bar_with_labels(counts_nuts2, "Cetnosti regionu CR")
#     props_nuts2 = (counts_nuts2 / counts_nuts2.sum()) if counts_nuts2.sum() else counts_nuts2.astype(float)
#     pasgr.pie_with_labels(props_nuts2, "Relativni cetnosti regionu CR")

#     # -------------------------------
#     # Spokojenost se životem (OV_1) - ordinální, opravené mapování
#     # -------------------------------

#     ov1_labels = [
#         "velmi spokojen", "spíše spokojen", "ani spokojen, ani nespokojen",
#         "spíše nespokojen", "velmi nespokojen"
#     ]
#     ov1_map = {i+1: lab for i, lab in enumerate(ov1_labels)}

#     ov_1_codes = pd.to_numeric(duvera["OV_1"], errors="coerce")
#     # Vezmi pouze 1..5, ostatní (0, 8, 9, 99…) → NaN
#     ov_1 = ov_1_codes.where(ov_1_codes.between(1, 5)).map(ov1_map)
#     ov_1 = pd.Categorical(ov_1, categories=ov1_labels, ordered=True)

#     print("OV_1 - unikátní hodnoty:")
#     print(pd.Series(ov_1).dropna().unique(), "\n")

#     ac_ov1 = pd.Series(ov_1).value_counts().reindex(ov1_labels, fill_value=0)
#     if ac_ov1.sum() == 0:
#         print("OV_1 - deskriptivní tabulka: žádná validní 1..5 data po očištění.\n")
#     else:
#         kac = ac_ov1.cumsum()
#         rc = (ac_ov1 / ac_ov1.sum()).round(2)
#         krc = rc.cumsum().round(2)
#         tab_ov1 = pd.DataFrame({"n(i)": ac_ov1, "N(i)": kac, "f(i)": rc, "F(i)": krc})
#         print("OV_1 - deskriptivní tabulka:")
#         print(tab_ov1, "\n")

#         pasgr.bar_with_labels(ac_ov1, "Spokojenost se zivotem")
#         pasgr.pie_with_labels(rc, "Spokojenost se zivotem (relativní)")

#     # -------------------------------
#     # Důvěra v média podle pohlaví
#     # -------------------------------

#     # pohlaví: 1 -> Muž, 2 -> Žena
#     pohlavi_codes = pd.to_numeric(duvera.get("IDE_8"), errors="coerce")
#     pohlavi = pohlavi_codes.map({1: "Muz", 2: "Zena"})

#     # PI_1z: ponech 1..4, ostatní NaN; mapuj na text
#     pi_labels = ["rozhodně důvěřuji", "spíše důvěřuji", "spíše nedůvěřuji", "rozhodně nedůvěřuji"]
#     pi_map = {i+1: lab for i, lab in enumerate(pi_labels)}
#     pi_codes = pd.to_numeric(duvera.get("PI_1z"), errors="coerce")
#     pi_clean = pi_codes.where(pi_codes.between(1, 4)).map(pi_map)

#     tab = pd.crosstab(pohlavi, pi_clean).reindex(columns=pi_labels, fill_value=0).dropna(how="all")
#     print("Tabulka pohlaví × důvěra v média:")
#     print(tab, "\n")

#     if tab.size and tab.to_numpy().sum() > 0:
#         row_props = tab.div(tab.sum(axis=1), axis=0).fillna(0).round(3)
#         print("Řádkové proporce (podíly v rámci pohlaví):")
#         print(row_props, "\n")

#         # [GRAF] Vstup: row_props
#         -
#         ax = row_props.plot(kind="bar", stacked=True, figsize=(8, 4))
#         ax.set_title("Duvera mediim podle pohlavi")
#         ax.set_ylabel("Podil")
#         ax.legend(title="Důvěra", bbox_to_anchor=(1.02, 1), loc="upper left")

#         plt.tight_layout()
#         plt.show()
#     else:
#         print("Kontingenční tabulka prázdná - zkontrolujte sloupce IDE_8 a PI_1z.\n")

#     # -------------------------------
#     # Číselné proměnné - Cars93 (pokud dataset existuje)
#     # -------------------------------

#     if cars is not None:
#         # Cylinders včetně 'rotary'
#         valce = cars["Cylinders"].astype(str)
#         ac_all = valce.value_counts().sort_index()
#         print("Cylinders - četnosti (včetně 'rotary'):")
#         print(ac_all, "\n")

#         # Bez 'rotary'
#         valce2 = valce[valce != "rotary"]
#         ac = valce2.value_counts().sort_index()
#         kac = ac.cumsum()
#         rc = (ac / ac.sum()).round(2) if ac.sum() else ac.astype(float)
#         krc = rc.cumsum().round(2) if ac.sum() else rc
#         tab_valce2 = pd.DataFrame({"n(i)": ac, "N(i)": kac, "f(i)": rc, "F(i)": krc})
#         print("Cylinders (bez 'rotary') - frekvenční rozdělení:")
#         print(tab_valce2, "\n")

#         # Frekvenční polygon pro valce2
#         # Pouze hodnoty, které lze převést na číslo:
#         x_vals = pd.to_numeric(ac.index, errors="coerce")
#         mask = ~x_vals.isna()
#         pasgr.freq_polygon(x_vals[mask], ac.values[mask], "Frekvencni polygon (Cylinders bez 'rotary')", "Pocet valcu")

#         # RPM - polygon + histogram
#         rpm = pd.to_numeric(cars["RPM"], errors="coerce").dropna()
#         ac_rpm = rpm.value_counts().sort_index()
#         pasgr.freq_polygon(ac_rpm.index, ac_rpm.values, "Frekvencni polygon proměnné RPM", "Otáčky motoru (RPM)")

#         -
#         plt.figure(figsize=(7, 4))
#         plt.hist(rpm, bins="auto", color="skyblue", edgecolor="darkblue")
#         plt.title("Histogram RPM")
#         plt.xlabel("Pocet otacek")
#         plt.ylabel("Absolutni cetnosti")
#         plt.tight_layout()
#         plt.show()

#         # Horsepower (hp) - histogramy, frekvenční rozdělení, boxploty, kvantily
#         hp = pd.to_numeric(cars["Horsepower"], errors="coerce").dropna()

#         # [GRAF] Vstup: hp
#         -
#         plt.figure(figsize=(7, 4))
#         plt.hist(hp, bins="auto", color="skyblue", edgecolor="darkblue")
#         plt.title("Histogram - Sila vozu (Horsepower)")
#         plt.xlabel("Sila vozu")
#         plt.ylabel("Absolutni cetnosti")
#         plt.tight_layout()
#         plt.show()

#         # [GRAF] Vstup: hp
#         -
#         plt.figure(figsize=(7, 4))
#         plt.hist(hp, bins=10, color="skyblue", edgecolor="darkblue")
#         plt.title("Histogram - Sila vozu (Horsepower), breaks = 10")
#         plt.xlabel("Sila vozu")
#         plt.ylabel("Absolutni cetnosti")
#         plt.tight_layout()
#         plt.show()

#         # [GRAF] Vstup: ac_hp
#         # Histogram summary table (not a plot, but related)
#         counts, breaks = np.histogram(hp, bins=10)
#         labels = [f"({breaks[i]:.0f}, {breaks[i+1]:.0f}]" for i in range(len(breaks)-1)]
#         ac_hp = pd.Series(counts, index=labels)
#         kac_hp = ac_hp.cumsum()
#         rc_hp = (ac_hp / ac_hp.sum()).round(3) if ac_hp.sum() else ac_hp.astype(float)
#         krc_hp = rc_hp.cumsum().round(3) if ac_hp.sum() else rc_hp
#         freq_hp = pd.DataFrame({"n(i)": ac_hp, "N(i)": kac_hp, "f(i)": rc_hp, "F(i)": krc_hp})
#         print("Horsepower - frekvenční rozdělení podle histogramu (10 tříd):")
#         print(freq_hp, "\n")

#         # Length - histogram + summary
#         length = pd.to_numeric(cars["Length"], errors="coerce").dropna()
#         print("Length - summary:")
#         print(length.describe(), "\n")

#         -
#         plt.figure(figsize=(7, 4))
#         plt.hist(length, bins=10, color="lightblue", edgecolor="darkblue")
#         plt.title("Histogram délky vozu")
#         plt.xlabel("Délka vozu (v palcích)")
#         plt.ylabel("Absolutni cetnosti")
#         plt.tight_layout()
#         plt.show()

#         # [GRAF] Vstup: hp
#         -
#         plt.figure(figsize=(5, 5))
#         plt.boxplot(hp, patch_artist=True,
#                     boxprops=dict(facecolor="yellow", edgecolor="orange"),
#                     medianprops=dict(color="black"))
#         plt.title("Krabicovy graf - Horsepower (s outliery)")
#         plt.ylabel("Sila vozu")
#         plt.tight_layout()
#         plt.show()

#         # Bez odlehlých (whis=3 ~ range=3 v R)
#         -
#         plt.figure(figsize=(5, 5))
#         plt.boxplot(hp, patch_artist=True, whis=3,
#                     boxprops=dict(facecolor="yellow", edgecolor="orange"),
#                     medianprops=dict(color="black"), showfliers=False)
#         plt.title("Krabicovy graf - Horsepower (bez odlehlých pozorování)")
#         plt.ylabel("Sila vozu")
#         plt.tight_layout()
#         plt.show()

#         # Kvantily, pěticíslo, průměr, summary
#         print("hp - min:", float(hp.min()))
#         print("hp - max:", float(hp.max()))
#         print("hp - Q1 (0.25):", float(hp.quantile(0.25)))
#         print("hp - Q3 (0.75):", float(hp.quantile(0.75)))
#         print("hp - median:", float(hp.median()))
#         five_num = [float(hp.min()), float(hp.quantile(0.25)), float(hp.median()),
#                     float(hp.quantile(0.75)), float(hp.max())]
#         print("hp - five-number summary [min, Q1, median, Q3, max]:")
#         print(five_num, "\n")
#         print("hp - mean:", float(hp.mean()))
#         print("hp - summary() ekvivalent:")
#         print(hp.describe(), "\n")

#         # Další proměnné: Length, Price, Weight
#         for var in ["Length", "Price", "Weight"]:
#             s = pd.to_numeric(cars[var], errors="coerce").dropna()
#             print(f"{var} - summary:")
#             print(s.describe(), "\n")

#             -
#             plt.figure(figsize=(7, 4))
#             plt.hist(s, bins=10, color="skyblue", edgecolor="darkblue")
#             plt.title(f"Histogram - {var}")
#             plt.xlabel(var)
#             plt.ylabel("Absolutni cetnosti")
#             plt.tight_layout()
#             plt.show()

#             plt.figure(figsize=(5, 5))
#             plt.boxplot(s, patch_artist=True,
#                         boxprops=dict(facecolor="khaki", edgecolor="saddlebrown"),
#                         medianprops=dict(color="black"))
#             plt.title(f"Krabicovy graf - {var}")
#             plt.ylabel(var)
#             plt.tight_layout()
#             plt.show()

#         # Porovnání skupin - cena podle původu
#         if "Origin" in cars.columns and "Price" in cars.columns:
#             puvod = cars["Origin"]
#             cena = pd.to_numeric(cars["Price"], errors="coerce")
#             grp_summary = cena.groupby(puvod).describe()
#             print("Cena podle původu (groupby/summary):")
#             print(grp_summary, "\n")

def cvika_3():
        # ---------------------------------------------------
    # 1. Načtení dat
    # ---------------------------------------------------
    policie = pd.read_csv("1_University\\3_semestr\\pas\\python-rewrite\\policie.csv", encoding="utf-8")

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
    pasgr.freq_polygon(x, y, "Frekvenční polygon – diastolický tlak", "Hodnota", "Počet")

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


if __name__ == "__main__":
   cvika_3()