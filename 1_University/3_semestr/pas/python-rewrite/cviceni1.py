import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

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

cum_table = pd.DataFrame({
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

# --- Sloupcový graf ---
counts = matur.value_counts().sort_index()
x_labels = counts.index.astype(str)
y_values = counts.values

plt.figure(figsize=(6, 4))
bars = plt.bar(x_labels, y_values, color=["#66c2a5", "#fc8d62"])
plt.title("Sloupcový graf – Maturita dříve")
plt.xlabel("Kategorie")
plt.ylabel("Počet")

# Popisky nad sloupci
for i, val in enumerate(y_values):
    plt.text(i, val + 0.5, str(val), ha='center', va='bottom')

plt.ylim(0, max(y_values) * 1.2)
plt.tight_layout()
plt.show()


# --- Koláčový graf bez popisků ---
plt.figure(figsize=(5, 5))
plt.pie(
    y_values,
    colors=["#66c2a5", "#fc8d62"],
    startangle=90,
)
plt.title("Koláčový graf – Maturita dříve")
plt.show()


# --- Koláčový graf s popisky (v procentech) ---
rel_perc = (counts / counts.sum() * 100).round(2)
labels_with_pct = [f"{lab} ({pct}%)" for lab, pct in zip(x_labels, rel_perc)]

plt.figure(figsize=(5, 5))
plt.pie(
    y_values,
    labels=labels_with_pct,
    colors=["#66c2a5", "#fc8d62"],
    startangle=90,
    autopct=None  # popisky máme ručně
)
plt.title("Koláčový graf s popisky – Maturita dříve")
plt.tight_layout()
plt.show()