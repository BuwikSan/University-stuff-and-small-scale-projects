import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


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
    # [GRAF] Vstup: counts (četnosti)
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
    # [GRAF] Vstup: props (proporce)
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
    # [GRAF] Vstup: x_vals, counts
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

# Univerzální funkce pro histogram
def histogram_with_labels(data, title="Histogram", bins="auto", color="skyblue", edgecolor="darkblue", xlabel="Hodnota", ylabel="Absolutni cetnosti", show=True, figsize=(7,4)):
    """
    Vykreslí histogram pro zadaná data.
    Parametry:
        data: pole nebo Series s číselnými hodnotami
        title: titulek grafu
        bins: počet tříd nebo 'auto'
        color: barva výplně
        edgecolor: barva okrajů
        xlabel, ylabel: popisky os
        show: zda zobrazit graf (True) nebo jen vrátit figuru (False)
        figsize: velikost obrázku
    """
    if data is None or len(data) == 0 or np.nansum(data) == 0:
        print(f"[SKIP] {title}: prázdné vstupní hodnoty.")
        return
    plt.figure(figsize=figsize)
    plt.hist(data, bins=bins, color=color, edgecolor=edgecolor)
    plt.title(title)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.tight_layout()
    if show:
        plt.show()
    else:
        return plt.gcf()

# Univerzální stacked barplot pro kontingenční/tabulkové proporce
def stacked_barplot(df, title="Stacked barplot", ylabel="Podíl", legend_title=None, figsize=(8,4), colors=None, legend_loc="upper left", legend_bbox=(1.02, 1)):
    """
    Vykreslí stacked barplot pro DataFrame s podíly (např. kontingenční tabulka).
    Parametry:
        df: DataFrame s podíly (řádky = skupiny, sloupce = kategorie)
        title: titulek grafu
        ylabel: popisek y-osy
        legend_title: titulek legendy
        figsize: velikost obrázku
        colors: seznam barev (volitelné)
        legend_loc: pozice legendy
        legend_bbox: anchor legendy
    """
    if df is None or df.size == 0 or np.nansum(df.values) == 0:
        print(f"[SKIP] {title}: prázdné vstupní hodnoty.")
        return
    ax = df.plot(kind="bar", stacked=True, figsize=figsize, color=colors)
    ax.set_title(title)
    ax.set_ylabel(ylabel)
    if legend_title:
        ax.legend(title=legend_title, bbox_to_anchor=legend_bbox, loc=legend_loc)
    else:
        ax.legend(bbox_to_anchor=legend_bbox, loc=legend_loc)
    plt.tight_layout()
    plt.show()

# Univerzální boxplot
def boxplot_with_labels(data, title="Boxplot", ylabel=None, xlabel=None, figsize=(5,5), color="yellow", edgecolor="orange", median_color="black", showfliers=True, whis=1.5, show=True):
    """
    Vykreslí boxplot pro zadaná data s volitelnými parametry.
    Parametry:
        data: pole nebo Series s číselnými hodnotami
        title: titulek grafu
        ylabel, xlabel: popisky os
        figsize: velikost obrázku
        color: barva výplně
        edgecolor: barva okrajů
        median_color: barva mediánu
        showfliers: zobrazit odlehlé hodnoty
        whis: rozsah pro "whiskers" (např. 1.5, nebo 3)
        show: zda zobrazit graf (True) nebo jen vrátit figuru (False)
    """
    if data is None or len(data) == 0 or np.nansum(data) == 0:
        print(f"[SKIP] {title}: prázdné vstupní hodnoty.")
        return
    plt.figure(figsize=figsize)
    plt.boxplot(data, patch_artist=True, whis=whis, showfliers=showfliers,
                boxprops=dict(facecolor=color, edgecolor=edgecolor),
                medianprops=dict(color=median_color))
    plt.title(title)
    if ylabel:
        plt.ylabel(ylabel)
    if xlabel:
        plt.xlabel(xlabel)
    plt.tight_layout()
    if show:
        plt.show()
    else:
        return plt.gcf()
