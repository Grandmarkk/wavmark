import librosa

def time_stretch_attack(signal, sample_rate, stretch_factor):
    """
    Perform a time-stretch attack on the watermarked audio signal.
    
    Parameters:
    signal (numpy array): The watermarked audio signal.
    sample_rate (int): The sample rate of the signal (e.g., 16000).
    stretch_factor (float): The factor by which to stretch/compress the signal.

    Returns:
    numpy array: The attacked signal (time-stretched).
    """
    attacked_signal = librosa.effects.time_stretch(signal, rate=stretch_factor)
    return attacked_signal