import sys

from time_stretch import time_stretch_attack # type: ignore
from plot_waveform import plot_waveforms # type: ignore

import numpy as np
import soundfile
import torch
import wavmark

# 1.load model
device = torch.device('cuda:0' if torch.cuda.is_available() else 'cpu')
model = wavmark.load_model().to(device)

# 2.create 16-bit payload
payload = np.random.choice([0, 1], size=16)
print("Payload:", payload)

# 3.read host audio
# the audio should be a single-channel 16kHz wav, you can read it using soundfile:
signal, sample_rate = soundfile.read("example.wav")
# Otherwise, you can use the following function to convert the host audio to single-channel 16kHz format:
# from wavmark.utils import file_reader
# signal = file_reader.read_as_single_channel("example.wav", aim_sr=16000)

# 4.encode watermark
watermarked_signal, _ = wavmark.encode_watermark(model, signal, payload, show_progress=True)

# you can save it as a new wav:
soundfile.write("watermarked_output.wav", watermarked_signal, 16000)


# 5. Perform the attack (e.g., time-stretching)
# Stretching by 0.75 will slow it down by 25%, or you can change the factor.
attacked_signal = time_stretch_attack(watermarked_signal, sample_rate, stretch_factor=0.75)
# Save the attacked signal
soundfile.write("attacked_output.wav", attacked_signal, 16000)
plot_waveforms(watermarked_signal, attacked_signal, sample_rate)

# 6.decode watermark
payload_decoded, _ = wavmark.decode_watermark(model, attacked_signal, show_progress=True)
print("Decoded Payload:", payload_decoded)
BER = (payload != payload_decoded).mean() * 100

print("Decode BER:%.1f" % BER)