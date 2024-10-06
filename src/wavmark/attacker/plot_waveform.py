import matplotlib.pyplot as plt
import numpy as np

def plot_waveforms(original_signal, attacked_signal, sample_rate):
    plt.figure(figsize=(12, 6))
    
    # Time axis for the signals
    time_original = np.linspace(0, len(original_signal) / sample_rate, num=len(original_signal))
    time_attacked = np.linspace(0, len(attacked_signal) / sample_rate, num=len(attacked_signal))

    # Plot original watermarked signal
    plt.subplot(2, 1, 1)
    plt.plot(time_original, original_signal, label='Watermarked Signal', color='b')
    plt.title('Watermarked Audio Signal')
    plt.xlabel('Time (seconds)')
    plt.ylabel('Amplitude')
    plt.xlim(0, len(original_signal) / sample_rate)
    plt.grid()
    plt.legend()

    # Plot attacked signal
    plt.subplot(2, 1, 2)
    plt.plot(time_attacked, attacked_signal, label='Attacked Signal', color='r')
    plt.title('Attacked Audio Signal')
    plt.xlabel('Time (seconds)')
    plt.ylabel('Amplitude')
    plt.xlim(0, len(attacked_signal) / sample_rate)
    plt.grid()
    plt.legend()

    plt.tight_layout()
    plt.show()