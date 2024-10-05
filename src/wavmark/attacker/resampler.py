import librosa
import soundfile as sf

def resample (file_path, sample_rate):
    y, sr = librosa.load(file_path, sr=None)  # sr=None keeps the original sampling rate

    # Resample the audio
    y_resampled = librosa.resample(y, orig_sr=sr, target_sr=sample_rate)

    # Save the resampled audio to a new file
    output_file = 'output.wav'
    sf.write(output_file, y_resampled, sample_rate)