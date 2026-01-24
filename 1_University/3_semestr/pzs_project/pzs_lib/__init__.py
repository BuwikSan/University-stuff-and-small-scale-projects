from .generators import generate_time_vector, sine_wave, square_wave, sawtooth_wave, add_noise
from .time_analysis import calculate_energy, statistics, autocorrelation, custom_convolution, find_peaks, resample_signal, normalize_signal
from .freq_analysis import dft_slow, get_frequency_spectrum, compute_real_cepstrum, analyze_voice_features
from .filters import design_fir_filter, apply_filter, moving_average
from .visualization import plot_time_signal, plot_spectrum, compare_signals