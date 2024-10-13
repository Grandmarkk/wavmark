import numpy as np

## Simulate random noise attack
def add_random_noise(audio_signal, noise_level):
    """
    Adds random noise to the audio signal.
    
    Args:
        audio_signal (numpy array): The input audio signal (1D for mono, 2D for stereo).
        noise_level (float): The standard deviation of the Gaussian noise to add 
                             (e.g., 0.01 for low noise, 0.1 for high noise).
        
    Returns:
        numpy array: The noisy audio signal.
    """
    # Generate random noise
    noise = np.random.normal(0, noise_level, audio_signal.shape)
    
    # Add the noise to the original signal
    noisy_signal = audio_signal + noise
    
    # Ensure the values stay within the valid range for audio (-1 to 1)
    noisy_signal = np.clip(noisy_signal, -1, 1)
    
    return noisy_signal


