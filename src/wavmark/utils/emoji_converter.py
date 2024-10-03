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