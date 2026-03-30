"""
Sada predefinovaných grafů pro analýzu ML projektů
Obsahuje funkce pro vizualizaci dat, výsledků modelů a porovnání transformací
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.metrics import confusion_matrix, roc_curve, auc
from typing import Union, List, Tuple, Dict, Optional


# ============================================================================
# 1. ANALÝZA DATOVÉHO SETU
# ============================================================================

def plot_feature_distributions(df: pd.DataFrame, columns: Optional[List[str]] = None,
                               figsize: Tuple[int, int] = (15, 10)) -> None:
    """
    Zobrazí histogramy distribucí všech numerických příznaků.

    Args:
        df: DataFrame s daty
        columns: Seznam sloupců k vykreslení (defaultně všechny numerické)
        figsize: Velikost figury
    """
    if columns is None:
        columns = df.select_dtypes(include=[np.number]).columns.tolist()

    n_cols = 3
    n_rows = (len(columns) + n_cols - 1) // n_cols
    fig, axes = plt.subplots(n_rows, n_cols, figsize=figsize)
    axes = axes.flatten()

    for idx, col in enumerate(columns):
        axes[idx].hist(df[col], bins=30, color='steelblue', alpha=0.7, edgecolor='black')
        axes[idx].set_title(f'Distribuce: {col}', fontweight='bold')
        axes[idx].set_xlabel('Hodnota')
        axes[idx].set_ylabel('Frekvence')
        axes[idx].grid(axis='y', alpha=0.3)

    # Skryj prázdné subploty
    for idx in range(len(columns), len(axes)):
        axes[idx].set_visible(False)

    plt.tight_layout()
    plt.show()


def plot_missing_data(df: pd.DataFrame, figsize: Tuple[int, int] = (12, 5)) -> None:
    """
    Zobrazí chybějící data v datasetu.

    Args:
        df: DataFrame
        figsize: Velikost figury
    """
    missing_data = df.isnull().sum()
    missing_percent = (missing_data / len(df)) * 100
    missing_df = pd.DataFrame({
        'Chybějící': missing_data,
        'Procent': missing_percent
    }).sort_values('Chybějící', ascending=False)

    missing_df = missing_df[missing_df['Chybějící'] > 0]

    if len(missing_df) == 0:
        print("✅ Žádná chybějící data!")
        return

    fig, ax = plt.subplots(figsize=figsize)
    missing_df['Chybějící'].plot(kind='barh', ax=ax, color='coral')
    ax.set_title('Chybějící data v datasetu', fontweight='bold', fontsize=12)
    ax.set_xlabel('Počet chybějících hodnot')
    plt.tight_layout()
    plt.show()


def plot_target_distribution(y: pd.Series, figsize: Tuple[int, int] = (10, 5)) -> None:
    """
    Zobrazí distribuci cílové proměnné (class balance).

    Args:
        y: Series s cílovou proměnnou
        figsize: Velikost figury
    """
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=figsize)

    # Počty
    counts = y.value_counts()
    ax1.bar(range(len(counts)), counts.values, color='steelblue', alpha=0.7, edgecolor='black')
    ax1.set_xticks(range(len(counts)))
    ax1.set_xticklabels(counts.index, rotation=45, ha='right')
    ax1.set_title('Počty vzorků v každé třídě', fontweight='bold')
    ax1.set_ylabel('Počet vzorků')
    ax1.grid(axis='y', alpha=0.3)

    # Procenta
    percentages = (counts / len(y)) * 100
    colors = sns.color_palette('Set2', len(counts))
    ax2.pie(percentages, labels=counts.index, autopct='%1.1f%%', colors=colors, startangle=90)
    ax2.set_title('Distribuce tříd (%)', fontweight='bold')

    plt.tight_layout()
    plt.show()


def plot_correlation_matrix(df: pd.DataFrame, figsize: Tuple[int, int] = (12, 10),
                            annot: bool = True, cmap: str = 'coolwarm') -> None:
    """
    Zobrazí korelační matici příznaků.

    Args:
        df: DataFrame s numerickými příznaky
        figsize: Velikost figury
        annot: Zobrazit hodnoty korelace
        cmap: Colormap
    """
    # Vyber jen numerické sloupce
    numeric_df = df.select_dtypes(include=[np.number])

    corr_matrix = numeric_df.corr()

    fig, ax = plt.subplots(figsize=figsize)
    sns.heatmap(corr_matrix, annot=annot, fmt='.2f', cmap=cmap, center=0,
                square=True, linewidths=0.5, cbar_kws={'label': 'Korelace'}, ax=ax)
    ax.set_title('Korelační matice příznaků', fontweight='bold', fontsize=14)
    plt.tight_layout()
    plt.show()


def plot_feature_statistics(df: pd.DataFrame, figsize: Tuple[int, int] = (14, 6)) -> None:
    """
    Zobrazí box ploty všech numerických příznaků.

    Args:
        df: DataFrame
        figsize: Velikost figury
    """
    numeric_df = df.select_dtypes(include=[np.number])

    fig, ax = plt.subplots(figsize=figsize)
    numeric_df.boxplot(ax=ax)
    ax.set_title('Statistika příznaků (Box plot)', fontweight='bold', fontsize=14)
    ax.set_ylabel('Hodnota')
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()
    plt.show()


# ============================================================================
# 2. ANALÝZA TRANSFORMACÍ
# ============================================================================

def plot_transformation_comparison(results_dict: Dict[str, Dict[str, float]],
                                   figsize: Tuple[int, int] = (14, 5)) -> None:
    """
    Porovnání různých transformací příznaků.

    Args:
        results_dict: Dict s výsledky transformací
                     Format: {'název': {'train_acc': x, 'test_acc': y, 'test_f1': z}}
        figsize: Velikost figury
    """
    fig, axes = plt.subplots(1, 2, figsize=figsize)

    names = list(results_dict.keys())
    train_accs = [results_dict[n]['train_acc'] for n in names]
    test_accs = [results_dict[n]['test_acc'] for n in names]
    test_f1s = [results_dict[n]['test_f1'] for n in names]

    x = np.arange(len(names))
    width = 0.35

    # Levý graf: Accuracy a F1-score
    axes[0].bar(x - width/2, test_accs, width, label='Accuracy', color='steelblue', alpha=0.8)
    axes[0].bar(x + width/2, test_f1s, width, label='F1-score', color='coral', alpha=0.8)
    axes[0].set_ylabel('Skóre')
    axes[0].set_title('Testovací metriky', fontweight='bold')
    axes[0].set_xticks(x)
    axes[0].set_xticklabels(names, rotation=15, ha='right', fontsize=9)
    axes[0].legend()
    axes[0].grid(axis='y', alpha=0.3)

    for i, (acc, f1) in enumerate(zip(test_accs, test_f1s)):
        axes[0].text(i - width/2, acc + 0.01, f'{acc:.3f}', ha='center', va='bottom', fontsize=8)
        axes[0].text(i + width/2, f1 + 0.01, f'{f1:.3f}', ha='center', va='bottom', fontsize=8)

    # Pravý graf: Overfitting check
    overfit = [t - te for t, te in zip(train_accs, test_accs)]
    colors = ['green' if o < 0.05 else 'orange' if o < 0.1 else 'red' for o in overfit]

    axes[1].bar(x, overfit, color=colors, alpha=0.7)
    axes[1].set_ylabel('Rozdíl (Trénovací - Testovací)')
    axes[1].set_title('Indikátor overfittingu', fontweight='bold')
    axes[1].set_xticks(x)
    axes[1].set_xticklabels(names, rotation=15, ha='right', fontsize=9)
    axes[1].axhline(y=0.05, color='orange', linestyle='--', alpha=0.5, label='Práh (0.05)')
    axes[1].grid(axis='y', alpha=0.3)
    axes[1].legend()

    for i, of in enumerate(overfit):
        axes[1].text(i, of + 0.003, f'{of:.3f}', ha='center', va='bottom', fontsize=8)

    plt.tight_layout()
    plt.show()


def plot_before_after_transformation(X_before: np.ndarray, X_after: np.ndarray,
                                      feature_names: Optional[List[str]] = None,
                                      figsize: Tuple[int, int] = (14, 5)) -> None:
    """
    Porovnání distribucí před a po transformaci.

    Args:
        X_before: Data před transformací
        X_after: Data po transformaci
        feature_names: Názvy příznaků (zobrazí se prvních 6)
        figsize: Velikost figury
    """
    n_features = min(6, X_before.shape[1])
    fig, axes = plt.subplots(2, n_features, figsize=figsize)

    if n_features == 1:
        axes = axes.reshape(2, 1)

    for i in range(n_features):
        # Před
        axes[0, i].hist(X_before[:, i], bins=30, color='steelblue', alpha=0.7, edgecolor='black')
        feat_name = feature_names[i] if feature_names else f'Příznak {i}'
        axes[0, i].set_title(f'Před: {feat_name}', fontsize=10)
        axes[0, i].grid(axis='y', alpha=0.3)

        # Po
        axes[1, i].hist(X_after[:, i], bins=30, color='coral', alpha=0.7, edgecolor='black')
        axes[1, i].set_title(f'Po: {feat_name}', fontsize=10)
        axes[1, i].grid(axis='y', alpha=0.3)

    plt.tight_layout()
    plt.show()


# ============================================================================
# 3. VÝSLEDKY MODELŮ
# ============================================================================

def plot_confusion_matrix(y_true: Union[np.ndarray, pd.Series],
                          y_pred: Union[np.ndarray, pd.Series],
                          class_names: Optional[List[str]] = None,
                          title: str = 'Confusion Matrix',
                          figsize: Tuple[int, int] = (8, 6)) -> None:
    """
    Zobrazí confusion matrix s hodnotami i procentuálním vyjádřením.

    Args:
        y_true: Správné predikce
        y_pred: Predikce modelu
        class_names: Názvy tříd
        title: Titulek grafu
        figsize: Velikost figury
    """
    cm = confusion_matrix(y_true, y_pred)

    if class_names is None:
        class_names = [str(i) for i in range(len(cm))]

    fig, ax = plt.subplots(figsize=figsize)

    # Normalizovaná matice pro heatmap (procenta)
    cm_norm = cm.astype('float') / cm.sum(axis=1)[:, np.newaxis]

    sns.heatmap(cm_norm, annot=cm, fmt='d', cmap='Blues', cbar=True,
                xticklabels=class_names, yticklabels=class_names, ax=ax,
                annot_kws={'size': 12, 'weight': 'bold'})

    ax.set_title(title, fontweight='bold', fontsize=14)
    ax.set_ylabel('Skutečná třída')
    ax.set_xlabel('Predikovaná třída')
    plt.tight_layout()
    plt.show()


def plot_model_metrics_comparison(models_results: Dict[str, Dict[str, float]],
                                  figsize: Tuple[int, int] = (14, 6)) -> None:
    """
    Porovnání metrik více modelů vedle sebe.

    Args:
        models_results: Dict s metrami modelů
                       Format: {'model_name': {'accuracy': x, 'precision': y, 'recall': z, 'f1': w}}
        figsize: Velikost figury
    """
    model_names = list(models_results.keys())
    metrics = list(models_results[model_names[0]].keys())

    x = np.arange(len(model_names))
    width = 0.2

    fig, ax = plt.subplots(figsize=figsize)

    for i, metric in enumerate(metrics):
        values = [models_results[model][metric] for model in model_names]
        ax.bar(x + i * width, values, width, label=metric, alpha=0.8)

    ax.set_ylabel('Skóre')
    ax.set_title('Porovnání metrik modelů', fontweight='bold', fontsize=14)
    ax.set_xticks(x + width * (len(metrics) - 1) / 2)
    ax.set_xticklabels(model_names, rotation=45, ha='right')
    ax.legend()
    ax.grid(axis='y', alpha=0.3)

    plt.tight_layout()
    plt.show()


def plot_roc_curve(y_true: Union[np.ndarray, pd.Series],
                   y_proba: np.ndarray,
                   class_idx: int = 1,
                   figsize: Tuple[int, int] = (8, 6)) -> float:
    """
    Zobrazí ROC křivku pro binární nebo vybranou třídu.

    Args:
        y_true: Správné predikce
        y_proba: Pravděpodobnosti tříd
        class_idx: Index třídy pro ROC (pro multi-class)
        figsize: Velikost figury

    Returns:
        AUC skóre
    """
    # Binární klasifikace
    if len(y_proba.shape) == 1 or y_proba.shape[1] == 1:
        y_true_bin = y_true
        y_proba_bin = y_proba if len(y_proba.shape) == 1 else y_proba[:, 0]
    else:
        # Multi-class - one-vs-rest
        classes = np.unique(y_true)
        y_true_bin = (y_true == classes[class_idx]).astype(int)
        y_proba_bin = y_proba[:, class_idx]

    fpr, tpr, _ = roc_curve(y_true_bin, y_proba_bin)
    roc_auc = auc(fpr, tpr)

    fig, ax = plt.subplots(figsize=figsize)
    ax.plot(fpr, tpr, color='steelblue', lw=2, label=f'ROC (AUC = {roc_auc:.3f})')
    ax.plot([0, 1], [0, 1], color='red', lw=2, linestyle='--', label='Random')
    ax.set_xlabel('False Positive Rate')
    ax.set_ylabel('True Positive Rate')
    ax.set_title('ROC Křivka', fontweight='bold', fontsize=14)
    ax.legend(loc='lower right')
    ax.grid(alpha=0.3)

    plt.tight_layout()
    plt.show()

    return roc_auc


def plot_feature_importance(coefficients: np.ndarray,
                           feature_names: List[str],
                           top_n: int = 15,
                           figsize: Tuple[int, int] = (10, 6)) -> None:
    """
    Zobrazí důležitost příznaků (např. z logistické regrese).

    Args:
        coefficients: Koeficienty modelu
        feature_names: Názvy příznaků
        top_n: Počet top příznaků k zobrazení
        figsize: Velikost figury
    """
    # Absolutní hodnoty
    coef_abs = np.abs(coefficients.flatten())

    # Seřaď a vezmi top_n
    top_indices = np.argsort(coef_abs)[-top_n:][::-1]
    top_features = [feature_names[i] for i in top_indices]
    top_coefs = coef_abs[top_indices]

    fig, ax = plt.subplots(figsize=figsize)
    colors = ['steelblue' if c > 0 else 'coral' for c in coefficients.flatten()[top_indices]]
    ax.barh(range(len(top_features)), top_coefs, color=colors, alpha=0.7, edgecolor='black')
    ax.set_yticks(range(len(top_features)))
    ax.set_yticklabels(top_features)
    ax.set_xlabel('Absolutní hodnota koeficientu')
    ax.set_title(f'Top {top_n} Důležitých Příznaků', fontweight='bold', fontsize=14)
    ax.invert_yaxis()
    ax.grid(axis='x', alpha=0.3)

    plt.tight_layout()
    plt.show()


# ============================================================================
# 4. DALŠÍ UTILITY
# ============================================================================

def plot_learning_curve(train_scores: List[float], val_scores: List[float],
                        figsize: Tuple[int, int] = (10, 6)) -> None:
    """
    Zobrazí learning curve (trénovací vs validační skóre).

    Args:
        train_scores: Skóre na trénovacích datech
        val_scores: Skóre na validačních datech
        figsize: Velikost figury
    """
    fig, ax = plt.subplots(figsize=figsize)

    epochs = range(1, len(train_scores) + 1)
    ax.plot(epochs, train_scores, 'o-', label='Trénování', color='steelblue', linewidth=2)
    ax.plot(epochs, val_scores, 's-', label='Validace', color='coral', linewidth=2)

    ax.set_xlabel('Epochs / Iterace')
    ax.set_ylabel('Skóre')
    ax.set_title('Learning Curve', fontweight='bold', fontsize=14)
    ax.legend()
    ax.grid(alpha=0.3)

    plt.tight_layout()
    plt.show()


def print_model_summary(y_true: Union[np.ndarray, pd.Series],
                        y_pred: Union[np.ndarray, pd.Series],
                        model_name: str = 'Model') -> None:
    """
    Vytiskne shrnutí výkonu modelu.

    Args:
        y_true: Správné predikce
        y_pred: Predikce modelu
        model_name: Název modelu
    """
    from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score

    acc = accuracy_score(y_true, y_pred)
    prec = precision_score(y_true, y_pred, average='weighted', zero_division=0)
    rec = recall_score(y_true, y_pred, average='weighted', zero_division=0)
    f1 = f1_score(y_true, y_pred, average='weighted', zero_division=0)

    print(f"\n{'='*50}")
    print(f"VÝSLEDKY: {model_name}")
    print(f"{'='*50}")
    print(f"Accuracy:  {acc:.4f} ({acc*100:.2f}%)")
    print(f"Precision: {prec:.4f}")
    print(f"Recall:    {rec:.4f}")
    print(f"F1-score:  {f1:.4f}")
    print(f"{'='*50}\n")
