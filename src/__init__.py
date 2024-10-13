import numpy as np
import soundfile
import torch
import wavmark
import tkinter as tk
from tkinter import scrolledtext, messagebox
import pygame
from wavmark.utils.emoji_converter import emoji_convert, binary_to_emoji
from wavmark.attacker.low_pass_filter import low_pass_filter_attack
from wavmark.attacker.echo_adder import add_echo
from wavmark.attacker.random_noise import add_random_noise
from wavmark.attacker.time_stretch import time_stretch_attack
from wavmark.utils import file_reader

# Initialize pygame for audio playback
pygame.mixer.init()

# Initialize the model and device
device = torch.device('cuda:0' if torch.cuda.is_available() else 'cpu')
model = wavmark.load_model().to(device)

# Global variables to store signals
original_signal = None
watermarked_signal = None
attacked_signal = None
selected_emoji = None
payload = None

# 16-bit emojis
emoji_list = ['⭐', '☀', '☁', '☔', '☕', '✈', '♡', '✂', '✉']

# Function to set selected emoji
def set_selected_emoji(emoji):
    global selected_emoji
    selected_emoji = emoji
    messagebox.showinfo("Emoji Selected", f"You have selected: {emoji}")

# Function to watermark the audio with the selected emoji
def watermark_audio():
    global watermarked_signal
    if not selected_emoji:
        messagebox.showerror("Error", "Please select an emoji first.")
        return
    binary_representation = emoji_convert(selected_emoji)
    payload = np.array([int(bit) for bit in binary_representation], dtype=np.int8)

    global original_signal
    original_signal, sample_rate = soundfile.read("example.wav")
    original_signal = file_reader.read_as_single_channel("example.wav", aim_sr=16000)
    
    # Encode watermark
    watermarked_signal, _ = wavmark.encode_watermark(model, original_signal, payload, show_progress=True)
    soundfile.write("watermarked_signal.wav", watermarked_signal, 16000)
    messagebox.showinfo("Success", "Watermark applied to audio.")

# Function to play original audio
def play_original_audio():
    pygame.mixer.music.load("example.wav")
    pygame.mixer.music.play()

# Function to play watermarked audio
def play_watermarked_audio():
    pygame.mixer.music.load("watermarked_signal.wav")
    pygame.mixer.music.play()

# Function to apply attacks to the watermarked audio
def apply_attack(attack_type):
    global attacked_signal
    if watermarked_signal is None:
        messagebox.showerror("Error", "Please watermark the audio first.")
        return
    if attack_type == 'low_pass':
        attacked_signal = low_pass_filter_attack(watermarked_signal, 16000, 7900)
    elif attack_type == 'echo':
        attacked_signal = add_echo(watermarked_signal, 16000)
    elif attack_type == 'time_stretch':
        attacked_signal = time_stretch_attack(watermarked_signal, 16000, 0.75)
    elif attack_type == 'random_noise':
        attacked_signal = add_random_noise(watermarked_signal, 0.1)
    
    soundfile.write("attacked_signal.wav", attacked_signal, 16000)
    messagebox.showinfo("Attack", f"{attack_type.replace('_', ' ').capitalize()} attack applied.")

# Function to play the attacked audio
def play_attacked_audio():
    if attacked_signal is None:
        messagebox.showerror("Error", "Please apply an attack first.")
        return
    pygame.mixer.music.load("attacked_signal.wav")
    pygame.mixer.music.play()

# Function to decode the attacked audio
def decode_attacked_audio():
    if attacked_signal is None:
        messagebox.showerror("Error", "Please apply an attack first.")
        return
    payload_decoded, _ = wavmark.decode_watermark(model, attacked_signal, show_progress=True)
    decoded_emoji = binary_to_emoji(payload_decoded)
    BER = (payload != payload_decoded).mean() * 100
    output_box.delete(1.0, tk.END)
    output_box.insert(tk.END, f"Decoded Emoji: {decoded_emoji}\n")
    output_box.insert(tk.END, f"Bit Error Rate (BER): {BER:.2f}%\n")

# Main GUI setup
root = tk.Tk()
root.title("Audio Watermarking System - Attack Simulator")
root.geometry("600x700")
root.configure(bg="#1C1C1C")  # Set background to dark gray

# Define font settings for thicker fonts
bold_font = ("Helvetica", 14, "bold")

# Top frame for selecting emojis
frame_emoji = tk.Frame(root, bg="#1C1C1C")
frame_emoji.pack(pady=10)

label_emoji = tk.Label(frame_emoji, text="Select an Emoji (16-bit only):", bg="#1C1C1C", fg="white", font=bold_font)
label_emoji.pack()

# Buttons for 16-bit emojis
for emoji in emoji_list:
    tk.Button(frame_emoji, text=emoji, command=lambda e=emoji: set_selected_emoji(e), bg="#FFD700", fg="black", font=bold_font).pack(side=tk.LEFT, padx=5)

# Labels and Buttons to play original audio
label_play_original = tk.Label(root, text="Listen to Original Audio:", bg="#1C1C1C", fg="white", font=bold_font)
label_play_original.pack(pady=10)
btn_play_original = tk.Button(root, text="Play Original Audio", command=play_original_audio, bg="#2E8B57", fg="white", font=bold_font)
btn_play_original.pack(pady=10)

# Labels and Buttons to watermark audio
label_watermark = tk.Label(root, text="Watermark Audio with Selected Emoji:", bg="#1C1C1C", fg="white", font=bold_font)
label_watermark.pack(pady=10)
btn_watermark = tk.Button(root, text="Watermark Audio", command=watermark_audio, bg="#2E8B57", fg="white", font=bold_font)
btn_watermark.pack(pady=10)

# Labels and Buttons to play watermarked audio
label_play_watermarked = tk.Label(root, text="Listen to Watermarked Audio:", bg="#1C1C1C", fg="white", font=bold_font)
label_play_watermarked.pack(pady=10)
btn_play_watermarked = tk.Button(root, text="Play Watermarked Audio", command=play_watermarked_audio, bg="#2E8B57", fg="white", font=bold_font)
btn_play_watermarked.pack(pady=10)

# Frame for attack buttons in a single row
frame_attack = tk.Frame(root, bg="#1C1C1C")
frame_attack.pack(pady=10)

label_attack = tk.Label(frame_attack, text="Select an Attack:", bg="#1C1C1C", fg="white", font=bold_font)
label_attack.grid(row=0, column=0, columnspan=4, pady=5)

# Buttons for different attacks in a single row
btn_low_pass = tk.Button(frame_attack, text="Low Pass Filter", command=lambda: apply_attack('low_pass'), bg="#2E8B57", fg="white", font=bold_font)
btn_low_pass.grid(row=1, column=0, padx=5, pady=5)

btn_echo = tk.Button(frame_attack, text="Echo", command=lambda: apply_attack('echo'), bg="#2E8B57", fg="white", font=bold_font)
btn_echo.grid(row=1, column=1, padx=5, pady=5)

btn_time_stretch = tk.Button(frame_attack, text="Time Stretch", command=lambda: apply_attack('time_stretch'), bg="#2E8B57", fg="white", font=bold_font)
btn_time_stretch.grid(row=1, column=2, padx=5, pady=5)

btn_random_noise = tk.Button(frame_attack, text="Random Noise", command=lambda: apply_attack('random_noise'), bg="#2E8B57", fg="white", font=bold_font)
btn_random_noise.grid(row=1, column=3, padx=5, pady=5)

# Labels and Buttons to play attacked audio
label_play_attacked = tk.Label(root, text="Listen to Attacked Audio:", bg="#1C1C1C", fg="white", font=bold_font)
label_play_attacked.pack(pady=10)
btn_play_attacked = tk.Button(root, text="Play Attacked Audio", command=play_attacked_audio, bg="#2E8B57", fg="white", font=bold_font)
btn_play_attacked.pack(pady=10)

# Labels and Buttons to decode the attacked audio
label_decode = tk.Label(root, text="Decode Attacked Audio:", bg="#1C1C1C", fg="white", font=bold_font)
label_decode.pack(pady=10)
btn_decode = tk.Button(root, text="Decode Attacked Audio", command=decode_attacked_audio, bg="#2E8B57", fg="white", font=bold_font)
btn_decode.pack(pady=10)

# Output text area for decoding result
output_box = scrolledtext.ScrolledText(root, wrap=tk.WORD, height=5, width=50, font=("Helvetica", 12), bg="black", fg="white")
output_box.pack(pady=10)

# Run the Tkinter event loop
root.mainloop()
