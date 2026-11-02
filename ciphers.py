import math

def vigenere_encrypt(text, key):
    result = []
    key_length = len(key)
    for i, char in enumerate(text):
        if char.isalpha():
            shift = ord(key[i % key_length].upper()) - ord('A')
            base = ord('A') if char.isupper() else ord('a')
            encrypted_char = chr((ord(char) - base + shift) % 26 + base)
            result.append(encrypted_char)
        else:
            result.append(char)
    return "".join(result)

def vigenere_decrypt(text, key):
    result = []
    key_length = len(key)
    for i, char in enumerate(text):
        if char.isalpha():
            shift = ord(key[i % key_length].upper()) - ord('A')
            base = ord('A') if char.isupper() else ord('a')
            decrypted_char = chr((ord(char) - base - shift + 26) % 26 + base)
            result.append(decrypted_char)
        else:
            result.append(char)
    return "".join(result)

def columnar_encrypt(text, key):
    # Only keep alphabets and convert to uppercase for clean transposition matrix
    text = "".join([c.upper() for c in text if c.isalpha()])
    key = key.upper()
    
    col_count = len(key)
    row_count = math.ceil(len(text) / col_count)
    
    # Pad with 'X' if necessary
    padding_len = (row_count * col_count) - len(text)
    text += 'X' * padding_len
    
    matrix = [list(text[i:i+col_count]) for i in range(0, len(text), col_count)]
    
    # Sort key alphabetically to get column read order
    sorted_key_indices = sorted(range(len(key)), key=lambda k: key[k])
    
    ciphertext = ""
    for idx in sorted_key_indices:
        for row in matrix:
            ciphertext += row[idx]
    return ciphertext

def columnar_decrypt(cipher, key):
    key = key.upper()
    col_count = len(key)
    row_count = math.ceil(len(cipher) / col_count)
    
    sorted_key_indices = sorted(range(len(key)), key=lambda k: key[k])
    
    # Recreate empty matrix grid
    matrix = [['' for _ in range(col_count)] for _ in range(row_count)]
    
    current_idx = 0
    # Fill columns back in sorted order
    for col_idx in sorted_key_indices:
        for r in range(row_count):
            if current_idx < len(cipher):
                matrix[r][col_idx] = cipher[current_idx]
                current_idx += 1
                
    # Read row by row to recover intermediate text
    plaintext = ""
    for row in matrix:
        plaintext += "".join(row)
    return plaintext

def custom_encrypt(plain, key):
    # Stage 1: Vigenere Substitution
    stage1 = vigenere_encrypt(plain, key)
    # Stage 2: Columnar Transposition
    stage2 = columnar_encrypt(stage1, key)
    return stage2

def custom_decrypt(cipher, key):
    # Stage 2 Reverse: Columnar Transposition Decryption
    stage1 = columnar_decrypt(cipher, key)
    # Stage 1 Reverse: Vigenere Decryption
    plain = vigenere_decrypt(stage1, key)
    return plain