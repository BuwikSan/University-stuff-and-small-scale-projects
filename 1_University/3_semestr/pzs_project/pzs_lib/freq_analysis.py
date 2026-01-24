import numpy as np

def dft_slow(x):
    """
    Vypočítá Diskrétní Fourierovu Transformaci (DFT) podle definice.
    Vhodné pro pochopení principu (jako v Tyden8.ipynb), ale pomalé pro dlouhé signály.
    """
    x = np.asarray(x, dtype=float)
    N = x.shape[0]
    n = np.arange(N)
    k = n.reshape((N, 1))
    # Matice exponenciál: e^(-i * 2*pi * k * n / N)
    M = np.exp(-2j * np.pi * k * n / N)
    return np.dot(M, x)

def get_frequency_spectrum(sig, fs):
    """
    Vrátí frekvenční osu a magnitudu spektra pomocí rychlé FFT.
    
    Returns:
        freqs: Osa frekvencí (Hz)
        magnitude: Amplituda spektra (normalizovaná)
    """
    N = len(sig)
    # FFT výpočet
    fft_vals = np.fft.fft(sig)
    
    # Frekvenční osa
    freqs = np.fft.fftfreq(N, 1/fs)
    
    # Vezmeme jen první polovinu (pozitivní frekvence)
    half_N = N // 2
    magnitude = np.abs(fft_vals[:half_N]) * (2.0 / N) # Normalizace amplitudy
    freqs = freqs[:half_N]
    
    return freqs, magnitude


def compute_real_cepstrum(sig):
    """
    Vypočítá reálné kepstrum signálu.
    Matematika: IFFT( log( |FFT(x)| ) )
    """
    # 1. Hammingovo okno (důležité pro vyhlazení okrajů u hlasu)
    window = np.hamming(len(sig))
    sig_windowed = sig * window
    
    # 2. FFT
    spectrum = np.fft.fft(sig_windowed)
    
    # 3. Logaritmus magnitudy
    log_spectrum = np.log(np.abs(spectrum) + 1e-10) # epsilon proti log(0)
    
    # 4. IFFT -> Kepstrum
    cepstrum_vals = np.fft.ifft(log_spectrum).real
    
    return cepstrum_vals

def analyze_voice_features(cepstrum_vals, fs, f_min=50, f_max=400):
    """
    Vytáhne z kepstra základní frekvenci (F0) a výraznost píku (CPP).
    
    Args:
        cepstrum_vals: Vypočítané kepstrum
        fs: Vzorkovací frekvence
        f_min, f_max: Rozsah frekvencí, kde hledáme lidský hlas (Hz)
        
    Returns:
        f0: Základní frekvence (Hz)
        cpp: Výška píku (Cepstral Peak Prominence) - určuje kvalitu hlasu
    """
    # Přepočet frekvence na quefrency (indexy)
    # Quefrency = fs / frekvence
    # Pozor: Nízká frekvence = Vysoká quefrency index
    min_index = int(fs / f_max) 
    max_index = int(fs / f_min)
    
    # Ochrana proti indexům mimo pole
    max_index = min(max_index, len(cepstrum_vals) // 2)
    
    # Vyřízneme jen tu část kepstra, kde může být hlas
    valid_region = cepstrum_vals[min_index:max_index]
    
    if len(valid_region) == 0:
        return 0.0, 0.0

    # Najdeme maximum v tomto regionu
    peak_idx_local = np.argmax(valid_region)
    cpp_value = valid_region[peak_idx_local]
    
    # Přepočteme lokální index zpět na globální index a pak na frekvenci
    peak_idx_global = min_index + peak_idx_local
    f0 = fs / peak_idx_global
    
    return f0, cpp_value