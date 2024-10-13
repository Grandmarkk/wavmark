import numpy as np

def add_echo(audio_signal, sample_rate, delay=500, attenuation=0.6):
    """
    Apply an echo effect to an audio signal.

    Parameters:
    audio_signal (numpy array): The input audio signal (1D for mono, 2D for stereo).
    sample_rate (int): The sample rate of the audio signal.
    delay (float): The delay of the echo in milliseconds. Default is 500 ms.
    attenuation (float): The attenuation (decay) factor of the echo. Default is 0.6.
    
    Returns:
    numpy array: The audio signal with the echo effect applied.
    """
    # Convert delay from milliseconds to samples
    delay_samples = int(delay * sample_rate / 1000)
    
    # Determine the max value for normalization based on the audio signal's data type
    if np.issubdtype(audio_signal.dtype, np.integer):
        max_val = np.iinfo(audio_signal.dtype).max
    elif np.issubdtype(audio_signal.dtype, np.floating):
        max_val = np.finfo(audio_signal.dtype).max
    else:
        raise ValueError("Unsupported audio signal data type")

    # Convert audio to float64 for processing
    audio_float = audio_signal.astype(np.float64) / max_val
    
    # Create a copy of the original audio
    echo_audio = np.copy(audio_float)
    
    # Add the echo effect
    if len(audio_signal.shape) == 1:  # Mono audio
        echo_audio[delay_samples:] += attenuation * audio_float[:-delay_samples]
    else:  # Stereo audio
        echo_audio[delay_samples:, 0] += attenuation * audio_float[:-delay_samples, 0]
        echo_audio[delay_samples:, 1] += attenuation * audio_float[:-delay_samples, 1]
    
    # Normalize the audio to prevent clipping
    echo_audio = np.clip(echo_audio, -1.0, 1.0)
    
    # Convert back to original data type
    echo_audio = (echo_audio * max_val).astype(audio_signal.dtype)
    
    return echo_audio

