import numpy as np
import soundfile
import torch
import wavmark
from wavmark.utils.emoji_converter import emoji_convert, binary_to_emoji
from wavmark.attacker.low_pass_filter import low_pass_filter_attack
from wavmark.attacker.echo_adder import add_echo
from wavmark.attacker.random_noise import add_random_noise
from wavmark.attacker.time_stretch import time_stretch_attack
from wavmark.utils import file_reader



# 1.load model
device = torch.device('cuda:0' if torch.cuda.is_available() else 'cpu')
model = wavmark.load_model().to(device)

# 2.create 16-bit payload
binary_representation = emoji_convert("⭐")
payload = np.array([int(bit) for bit in binary_representation], dtype=np.int8)
print("Payload:", payload)
print(binary_to_emoji(payload))

# 3.read host audio
# the audio should be a single-channel 16kHz wav, you can read it using soundfile:
signal, sample_rate = soundfile.read("example.wav")
# Otherwise, you can use the following function to convert the host audio to single-channel 16kHz format:
# from wavmark.utils import file_reader
signal = file_reader.read_as_single_channel("example.wav", aim_sr=16000)

# 4.encode watermark
watermarked_signal, _ = wavmark.encode_watermark(model, signal, payload, show_progress=True)
# save it as a new wav:
soundfile.write("watermaked_signal.wav", watermarked_signal, 16000)

## attack watermarked audio
attacked_signal = low_pass_filter_attack(watermarked_signal, sample_rate, 7900)
attacked_signal = add_echo(attacked_signal, sample_rate)
attacked_signal = time_stretch_attack(attacked_signal, sample_rate, 0.75)
# attacked_signal = add_random_noise(attacked_signal, 0.004)
soundfile.write("attacked_output.wav", attacked_signal, 16000)

# 5.decode watermark
payload_decoded, info = wavmark.decode_watermark(model, attacked_signal, show_progress=True)
BER = (payload != payload_decoded).mean() * 100

print(payload_decoded)
print(binary_to_emoji(payload_decoded))
print("Decode BER:%.1f" % BER)