import numpy as np
import matplotlib.pyplot as plt
import librosa.display

def plot_comparison_with_frequency(original_signal, filtered_signal, sample_rate):
    # Create a time axis
    time_axis = np.linspace(0, len(original_signal) / sample_rate, num=len(original_signal))

    # Plot spectrograms (frequency-domain)
    plt.figure(figsize=(12, 8))

    # Original Signal Spectrogram
    plt.subplot(2, 1, 1)
    D_orig = librosa.amplitude_to_db(np.abs(librosa.stft(original_signal)), ref=np.max)
    librosa.display.specshow(D_orig, sr=sample_rate, x_axis='time', y_axis='log')
    plt.title('Original Signal Spectrogram')
    plt.colorbar(format='%+2.0f dB')
    
    # Filtered Signal Spectrogram
    plt.subplot(2, 1, 2)
    D_filtered = librosa.amplitude_to_db(np.abs(librosa.stft(filtered_signal)), ref=np.max)
    librosa.display.specshow(D_filtered, sr=sample_rate, x_axis='time', y_axis='log')
    plt.title('Filtered Signal Spectrogram')
    plt.colorbar(format='%+2.0f dB')

    plt.tight_layout()
    plt.show()

    # Plot Frequency Response (Fourier Transform)
    plt.figure(figsize=(12, 6))

    # Compute FFT of the original and filtered signals
    freq_axis = np.fft.rfftfreq(len(original_signal), d=1/sample_rate)
    fft_orig = np.abs(np.fft.rfft(original_signal))
    fft_filtered = np.abs(np.fft.rfft(filtered_signal))

    # Plot original vs filtered frequency response
    plt.plot(freq_axis, fft_orig, label='Original Signal FFT', alpha=0.7)
    plt.plot(freq_axis, fft_filtered, label='Filtered Signal FFT', color='red', alpha=0.7)
    plt.title('Frequency Domain Comparison (FFT)')
    plt.xlabel('Frequency [Hz]')
    plt.ylabel('Amplitude')
    plt.legend()
    plt.grid()

    plt.tight_layout()
    plt.show()
