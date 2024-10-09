import numpy as np
import soundfile as sf

## Simulate random noise attack
def add_random_noise(file_path, noise_level):
    """
    Adds random noise to the audio signal.
    
    Args:
        file_path (numpy array): The input watermarked audio signal.
        noise_level (float): The level of noise to add (e.g., 0.01 for low noise, 0.1 for high noise).
        
    Returns:
        numpy array: The noisy audio signal.
    """
    # Generate random noise
    noise = np.random.normal(0, noise_level, file_path.shape)
    
    # Add the noise to the original signal
    noisy_signal = file_path + noise
    
    # Ensure the values stay within the valid range for audio (-1 to 1)
    noisy_signal = np.clip(noisy_signal, -1, 1)
    
    return noisy_signal
