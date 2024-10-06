import numpy as np
import soundfile
import torch
import wavmark
from wavmark.utils.emoji_converter import emoji_convert
from wavmark.attacker.echo_adder import add_echo


# 1.load model
device = torch.device('cuda:0' if torch.cuda.is_available() else 'cpu')
model = wavmark.load_model().to(device)

# 2.create 16-bit payload
binary_representation = emoji_convert("⭐")
payload = random_binary_array = np.array([int(bit) for bit in binary_representation], dtype=np.int8)
print("Payload:", payload)

# 3.read host audio
# the audio should be a single-channel 16kHz wav, you can read it using soundfile:
signal, sample_rate = soundfile.read("example.wav")
# Otherwise, you can use the following function to convert the host audio to single-channel 16kHz format:
# from wavmark.utils import file_reader
# signal = file_reader.read_as_single_channel("example.wav", aim_sr=16000)

# 4.encode watermark
watermarked_signal, _ = wavmark.encode_watermark(model, signal, payload, show_progress=True)
# save it as a new wav:
soundfile.write("output.wav", watermarked_signal, 16000)

## attack watermarked audio
add_echo("output.wav")

# 5.decode watermark
watermarked_signal, sample_rate = soundfile.read("output.wav")
payload_decoded, _ = wavmark.decode_watermark(model, watermarked_signal, show_progress=True)
BER = (payload != payload_decoded).mean() * 100

print(payload_decoded)
print("Decode BER:%.1f" % BER)