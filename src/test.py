from wavmark.utils.emoji_converter import emoji_convert, binary_to_emoji


def get_emoji_list():
    emojis = []
    
    # Define the Unicode ranges where emojis are commonly found
    emoji_ranges = [
        (0x1F300, 0x1F5FF),  # Miscellaneous Symbols and Pictographs
        (0x1F600, 0x1F64F),  # Emoticons (faces)
        (0x1F680, 0x1F6FF),  # Transport and Map Symbols
        (0x2600, 0x26FF),    # Miscellaneous Symbols
        (0x2700, 0x27BF),    # Dingbats
        (0x1F900, 0x1F9FF)   # Supplemental Symbols and Pictographs
    ]

    for start, end in emoji_ranges:
        for codepoint in range(start, end + 1):
            try:
                emojis.append(chr(codepoint))
            except:
                pass

    return emojis

# Get the emoji list and print
emoji_list = get_emoji_list()
print(emoji_list)
