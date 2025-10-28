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
