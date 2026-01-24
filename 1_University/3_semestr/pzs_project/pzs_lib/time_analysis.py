import numpy as np
import scipy.signal as signal

def calculate_energy(sig):
    """Vypočítá energii diskrétního signálu: suma(|x|^2)."""
    return np.sum(np.abs(sig)**2)

def calculate_power(sig):
    """Vypočítá střední výkon signálu: 1/N * suma(|x|^2)."""
    return np.mean(np.abs(sig)**2)

def statistics(sig):
    """Vrátí základní statistiky: mean, var, std."""
    return {
        "mean": np.mean(sig),
        "variance": np.var(sig),
        "std_dev": np.std(sig),
        "min": np.min(sig),
        "max": np.max(sig)
    }

def custom_convolution(sig1, sig2, mode='full'):
    """Wrapper pro konvoluci."""
    return np.convolve(sig1, sig2, mode=mode)

def autocorrelation(sig):
    """Vypočítá autokorelaci signálu."""
    # Použijeme korelaci signálu se sebou samým
    result = np.correlate(sig, sig, mode='full')
    return result[result.size // 2:] # Vracíme jen kladnou část zpoždění (lags)

def cross_correlation(sig1, sig2):
    """Vypočítá křížovou korelaci dvou signálů."""
    return np.correlate(sig1, sig2, mode='full')

def find_peaks(sig, height=None, distance=None):
    """
    Najde indexy vrcholů v signálu (např. R-vlny v EKG).
    Wrapper pro scipy.signal.find_peaks.
    
    Args:
        sig: Vstupní signál
        height: Minimální výška vrcholu (práh)
        distance: Minimální vzdálenost mezi vrcholy ve vzorcích
    Returns:
        peaks: Pole indexů, kde jsou vrcholy
    """
    peaks, _ = signal.find_peaks(sig, height=height, distance=distance)
    return peaks

def resample_signal(sig, original_fs, target_fs):
    """
    Převzorkuje signál na novou frekvenci.
    Nutné pro korelaci signálů s různým fs (jak je v zadání I).
    """
    if original_fs == target_fs:
        return sig
    
    duration = len(sig) / original_fs
    target_samples = int(duration * target_fs)
    
    return signal.resample(sig, target_samples)

def normalize_signal(sig):
    """
    Normalizuje signál do rozsahu -1 až 1 (nebo 0 až 1).
    Hodí se pro porovnávání tvarů (korelace).
    """
    # Odstranění stejnosměrné složky (centrování)
    sig_centered = sig - np.mean(sig)
    # Normalizace podle maxima absolutní hodnoty
    return sig_centered / np.max(np.abs(sig_centered))