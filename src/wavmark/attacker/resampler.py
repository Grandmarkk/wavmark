import librosa

def resample(audio_signal, orig_sample_rate, target_sample_rate):
    """
    Resamples the given audio signal to a new sample rate.

    Args:
        audio_signal (numpy array): The input audio signal.
        orig_sample_rate (int): The original sample rate of the audio signal.
        target_sample_rate (int): The desired sample rate for the resampled audio.
        
    Returns:
        numpy array: The resampled audio signal.
    """
    # Resample the audio signal
    y_resampled = librosa.resample(audio_signal, orig_sr=orig_sample_rate, target_sr=target_sample_rate)
    
    return y_resampled
