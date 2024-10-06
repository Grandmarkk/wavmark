import numpy as np
from scipy.io import wavfile
import soundfile as sf

def add_echo(file_path, delay=500, attenuation=0.6):
    # Read the input audio file
    sample_rate, audio = wavfile.read(file_path)
    
    # Convert delay from milliseconds to samples
    delay_samples = int(delay * sample_rate / 1000)
    
    # Convert audio to float64 for processing
    audio_float = audio.astype(np.float64) / np.iinfo(audio.dtype).max
    
    # Create a copy of the original audio
    echo_audio = np.copy(audio_float)
    
    # Add the echo effect
    if len(audio.shape) == 1:  # Mono audio
        echo_audio[delay_samples:] += attenuation * audio_float[:-delay_samples]
    else:  # Stereo audio
        echo_audio[delay_samples:, 0] += attenuation * audio_float[:-delay_samples, 0]
        echo_audio[delay_samples:, 1] += attenuation * audio_float[:-delay_samples, 1]
    
    # Normalize the audio to prevent clipping
    echo_audio = np.clip(echo_audio, -1.0, 1.0)
    
    # Convert back to original data type
    echo_audio = (echo_audio * np.iinfo(audio.dtype).max).astype(audio.dtype)
    
    
    # Save the processed audio
    output_file = 'output.wav'
    sf.write(output_file, echo_audio, sample_rate)