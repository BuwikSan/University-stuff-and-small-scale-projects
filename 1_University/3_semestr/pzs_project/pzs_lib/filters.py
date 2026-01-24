import numpy as np
import scipy.signal as signal

def design_fir_filter(fs, cutoff_freq, num_taps=None, ripple_db=60.0, width_hz=None):
    """
    Navrhne koeficienty FIR filtru (typ dolní propust).
    Pokud není zadáno num_taps, vypočítá se automaticky pomocí Kaiserova vzorce.
    
    Args:
        fs: Vzorkovací frekvence
        cutoff_freq: Mezní frekvence (Hz)
        ripple_db: Útlum v nepropustném pásmu (dB) - default 60dB
        width_hz: Šířka přechodového pásma (Hz)
    """
    nyq_rate = fs / 2.0
    
    # Pokud není zadán počet tapů, odhadneme ho (jako v notebooku)
    if num_taps is None:
        if width_hz is None:
            width_hz = 5.0 # Defaultní šířka přechodu
        width = width_hz / nyq_rate
        # Funkce kaiserord vrátí potřebný řád filtru a beta parametr
        num_taps, beta = signal.kaiserord(ripple_db, width)
        # num_taps musí být liché pro symetrický FIR filtr typu I
        if num_taps % 2 == 0:
            num_taps += 1
    else:
        beta = 0.1102 * (ripple_db - 8.7) if ripple_db > 50 else 0.5842 * (ripple_db - 21) ** 0.4 + 0.07886 * (ripple_db - 21)
    
    # Výpočet koeficientů
    taps = signal.firwin(num_taps, cutoff_freq/nyq_rate, window=('kaiser', beta))
    return taps

def apply_filter(sig, taps):
    """Aplikuje FIR filtr na signál pomocí konvoluce (lfilter)."""
    # a=1.0 protože u FIR filtru jmenovatel přenosové funkce neexistuje
    return signal.lfilter(taps, 1.0, sig)

def moving_average(sig, window_size=5):
    """Jednoduchý filtr klouzavého průměru."""
    window = np.ones(window_size) / window_size
    return np.convolve(sig, window, mode='same')