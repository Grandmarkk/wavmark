import numpy as np

def emoji_convert(emoji):
    '''
    Convert a 2-byte emoji to a 16-bit binary array

    Args: 
        emoji: a 2-byte emoji

    Return: 
        the 16-bit binary representation of the input emoji
    '''
    
    code_point = ord(emoji)

    binary_representation = format(code_point, '016b')

    return binary_representation


def binary_to_emoji(binary_array):
    '''
    Convert a 1D numpy array storing the 16-bit binary representation back to an emoji.
    
    Args:
        binary_array: 1D numpy array of binary digits (0s and 1s) representing the emoji.
    
    Return:
        The corresponding emoji as a character.
    '''
    
    # Convert binary array to a string representation
    binary_string = ''.join(binary_array.astype(str))
    
    # Convert the binary string back to a Unicode code point (integer)
    code_point = int(binary_string, 2)
    
    # Convert the Unicode code point to the corresponding emoji
    emoji = chr(code_point)
    
    return emoji