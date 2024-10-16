import numpy as np
import soundfile
import torch
import wavmark
import tkinter as tk
from tkinter import scrolledtext, messagebox
import pygame
from wavmark.utils.emoji_converter import emoji_convert, binary_to_emoji
from wavmark.attacker.low_pass_filter import low_pass_filter_attack
from wavmark.attacker.random_noise import add_random_noise
from wavmark.attacker.time_stretch import time_stretch_attack
from wavmark.utils import file_reader
import librosa

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

# Resample function
def resample(audio_signal, orig_sample_rate, target_sample_rate):
    """
    Resamples the given audio signal to a new sample rate.
    """
    return librosa.resample(audio_signal, orig_sr=orig_sample_rate, target_sr=target_sample_rate)

# Echo function
def add_echo(audio_signal, sample_rate, delay=500, attenuation=0.6):
    """
    Apply an echo effect to an audio signal.
    """
    delay_samples = int(delay * sample_rate / 1000)
    audio_float = audio_signal.astype(np.float64)
    echo_audio = np.copy(audio_float)
    
    if len(audio_signal.shape) == 1:  # Mono audio
        echo_audio[delay_samples:] += attenuation * audio_float[:-delay_samples]
    else:  # Stereo audio
        echo_audio[delay_samples:, 0] += attenuation * audio_float[:-delay_samples, 0]
        echo_audio[delay_samples:, 1] += attenuation * audio_float[:-delay_samples, 1]
    
    echo_audio = np.clip(echo_audio, -1.0, 1.0)
    return echo_audio

# Function to apply attacks to the watermarked audio
def apply_attack(attack_type, parameter=None):
    global attacked_signal
    if watermarked_signal is None:
        messagebox.showerror("Error", "Please watermark the audio first.")
        return
    try:
        if attack_type == 'low_pass':
            parameter = float(parameter)
            attacked_signal = low_pass_filter_attack(watermarked_signal, 16000, parameter)
        elif attack_type == 'echo':
            attacked_signal = add_echo(watermarked_signal, 16000)
        elif attack_type == 'time_stretch':
            parameter = float(parameter)
            attacked_signal = time_stretch_attack(watermarked_signal, 16000, parameter)
        elif attack_type == 'random_noise':
            parameter = float(parameter)
            attacked_signal = add_random_noise(watermarked_signal, parameter)
        elif attack_type == 'resample':
            parameter = int(parameter)
            attacked_signal = resample(watermarked_signal, 16000, parameter)
        
        soundfile.write("attacked_signal.wav", attacked_signal, 16000)
        messagebox.showinfo("Attack", f"{attack_type.replace('_', ' ').capitalize()} attack applied.")
    except ValueError:
        messagebox.showerror("Error", "Invalid input for the attack parameter.")

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
    
    output_box.delete(1.0, tk.END)  # Clear the output box before showing new results
    
    if payload_decoded is None:
        output_box.insert(tk.END, "Can't retrieve watermark, BER: 100%\n")
    else:
        decoded_emoji = binary_to_emoji(payload_decoded)
        BER = (payload != payload_decoded).mean() * 100
        output_box.insert(tk.END, f"Decoded Emoji: {decoded_emoji}\n")
        output_box.insert(tk.END, f"Bit Error Rate (BER): {BER:.2f}%\n")


# Main GUI setup with scrolling functionality
root = tk.Tk()
root.title("Audio Watermarking System - Attack Simulator")
root.geometry("600x800")
root.configure(bg="#1C1C1C")  # Set background to dark gray

# Create a canvas for scrolling
canvas = tk.Canvas(root, borderwidth=0, background="#1C1C1C")
scroll_frame = tk.Frame(canvas, bg="#1C1C1C")
scrollbar = tk.Scrollbar(root, orient="vertical", command=canvas.yview)
canvas.configure(yscrollcommand=scrollbar.set)

scrollbar.pack(side="right", fill="y")
canvas.pack(side="left", fill="both", expand=True)
canvas.create_window((0, 0), window=scroll_frame, anchor="n")  # anchor to the top center

# Configure the scroll region of the canvas
def onFrameConfigure(canvas):
    canvas.configure(scrollregion=canvas.bbox("all"))

scroll_frame.bind("<Configure>", lambda event, canvas=canvas: onFrameConfigure(canvas))

# Define font settings for thicker fonts
bold_font = ("Helvetica", 14, "bold")

# Center-align elements
label_options = {"bg": "#1C1C1C", "fg": "white", "font": bold_font}
btn_options = {"bg": "#2E8B57", "fg": "white", "font": bold_font}

# Top frame for selecting emojis
frame_emoji = tk.Frame(scroll_frame, bg="#1C1C1C")
frame_emoji.pack(pady=10)

label_emoji = tk.Label(frame_emoji, text="Select an Emoji (16-bit only):", **label_options)
label_emoji.pack(anchor="center")

# Buttons for 16-bit emojis
for emoji in emoji_list:
    tk.Button(frame_emoji, text=emoji, command=lambda e=emoji: set_selected_emoji(e), bg="#FFD700", fg="black", font=bold_font).pack(side=tk.LEFT, padx=5)

# Labels and Buttons to play original audio
label_play_original = tk.Label(scroll_frame, text="Listen to Original Audio:", **label_options)
label_play_original.pack(pady=10, anchor="center")
btn_play_original = tk.Button(scroll_frame, text="Play Original Audio", command=play_original_audio, **btn_options)
btn_play_original.pack(pady=10, anchor="center")

# Labels and Buttons to watermark audio
label_watermark = tk.Label(scroll_frame, text="Watermark Audio with Selected Emoji:", **label_options)
label_watermark.pack(pady=10, anchor="center")
btn_watermark = tk.Button(scroll_frame, text="Watermark Audio", command=watermark_audio, **btn_options)
btn_watermark.pack(pady=10, anchor="center")

# Labels and Buttons to play watermarked audio
label_play_watermarked = tk.Label(scroll_frame, text="Listen to Watermarked Audio:", **label_options)
label_play_watermarked.pack(pady=10, anchor="center")
btn_play_watermarked = tk.Button(scroll_frame, text="Play Watermarked Audio", command=play_watermarked_audio, **btn_options)
btn_play_watermarked.pack(pady=10, anchor="center")

# Frame for attack buttons and parameter inputs in a single row
frame_attack = tk.Frame(scroll_frame, bg="#1C1C1C")
frame_attack.pack(pady=10, anchor="center")

label_attack = tk.Label(frame_attack, text="Select an Attack and Input Parameters:", **label_options)
label_attack.grid(row=0, column=0, columnspan=6, pady=5, sticky="ew")

# Low Pass Filter attack with input box for cutoff frequency
tk.Label(frame_attack, text="Low Pass Filter (0 to 7900 Hz):", **label_options).grid(row=1, column=0)
entry_low_pass = tk.Entry(frame_attack)
entry_low_pass.grid(row=1, column=1)
btn_low_pass = tk.Button(frame_attack, text="Apply", command=lambda: apply_attack('low_pass', entry_low_pass.get()), **btn_options)
btn_low_pass.grid(row=1, column=2, padx=5, pady=5)

# Random Noise attack with input box for noise level
tk.Label(frame_attack, text="Random Noise (0 to 1):", **label_options).grid(row=2, column=0)
entry_random_noise = tk.Entry(frame_attack)
entry_random_noise.grid(row=2, column=1)
btn_random_noise = tk.Button(frame_attack, text="Apply", command=lambda: apply_attack('random_noise', entry_random_noise.get()), **btn_options)
btn_random_noise.grid(row=2, column=2, padx=5, pady=5)

# Time Stretch attack with input box for stretch factor
tk.Label(frame_attack, text="Time Stretch (0.5 to 2):", **label_options).grid(row=3, column=0)
entry_time_stretch = tk.Entry(frame_attack)
entry_time_stretch.grid(row=3, column=1)
btn_time_stretch = tk.Button(frame_attack, text="Apply", command=lambda: apply_attack('time_stretch', entry_time_stretch.get()), **btn_options)
btn_time_stretch.grid(row=3, column=2, padx=5, pady=5)

# Resample attack with input box for target sample rate
tk.Label(frame_attack, text="Resample (target sample rate):", **label_options).grid(row=4, column=0)
entry_resample = tk.Entry(frame_attack)
entry_resample.grid(row=4, column=1)
btn_resample = tk.Button(frame_attack, text="Apply", command=lambda: apply_attack('resample', entry_resample.get()), **btn_options)
btn_resample.grid(row=4, column=2, padx=5, pady=5)

# Echo attack (no input box needed)
btn_echo = tk.Button(frame_attack, text="Apply Echo", command=lambda: apply_attack('echo'), **btn_options)
btn_echo.grid(row=5, column=0, columnspan=3, padx=5, pady=5)

# Labels and Buttons to play attacked audio
label_play_attacked = tk.Label(scroll_frame, text="Listen to Attacked Audio:", **label_options)
label_play_attacked.pack(pady=10, anchor="center")
btn_play_attacked = tk.Button(scroll_frame, text="Play Attacked Audio", command=play_attacked_audio, **btn_options)
btn_play_attacked.pack(pady=10, anchor="center")

# Labels and Buttons to decode the attacked audio
label_decode = tk.Label(scroll_frame, text="Decode Attacked Audio:", **label_options)
label_decode.pack(pady=10, anchor="center")
btn_decode = tk.Button(scroll_frame, text="Decode Attacked Audio", command=decode_attacked_audio, **btn_options)
btn_decode.pack(pady=10, anchor="center")

# Output text area for decoding result
output_box = scrolledtext.ScrolledText(scroll_frame, wrap=tk.WORD, height=5, width=50, font=("Helvetica", 12), bg="black", fg="white")
output_box.pack(pady=10, anchor="center")

# Run the Tkinter event loop
root.mainloop()


