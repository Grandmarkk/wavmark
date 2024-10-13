import numpy as np
from scipy import signal

def low_pass_filter_attack(audio_signal, sample_rate, cutoff_freq, order=5):
    """
    Apply a low-pass filter to the audio signal.
    
    Parameters:
    audio_signal (numpy array): The input audio signal.
    sample_rate (int): The sample rate of the signal (e.g., 16000).
    cutoff_freq (float): The cutoff frequency of the low-pass filter.
    order (int): The order of the filter. Default is 5.
    
    Returns:
    numpy array: The filtered signal with the same length as the original.
    """
    # Normalize the cutoff frequency
    nyquist = 0.5 * sample_rate
    normal_cutoff = cutoff_freq / nyquist
    
    # Design the low-pass filter
    b, a = signal.butter(order, normal_cutoff, btype='low', analog=False)
    
    # Apply the filter forward and backward to prevent phase shift and extra padding
    filtered_signal = signal.filtfilt(b, a, audio_signal)
    
    return filtered_signal

