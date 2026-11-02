import math

# Stage 1: Vigenere Cipher (Polyalphabetic Substitution)
def vigenere_cipher(text, key, encrypt=True):
    result = []
    key = key.upper()
    key_idx = 0
    for char in text:
        if char.isalpha():
            shift = ord(key[key_idx % len(key)]) - ord('A')
            if not encrypt:
                shift = -shift
            
            base = ord('A') if char.isupper() else ord('a')
            new_char = chr((ord(char) - base + shift) % 26 + base)
            result.append(new_char)
            key_idx += 1
        else:
            result.append(char)
    return "".join(result)

# Stage 2: Columnar Transposition
def transposition_encrypt(text, key):
    ciphertext = [""] * len(key)
    for col in range(len(key)):
        pointer = col
        while pointer < len(text):
            ciphertext[col] += text[pointer]
            pointer += len(key)
    return "".join(ciphertext)

def transposition_decrypt(ciphertext, key):
    num_cols = len(key)
    num_rows = math.ceil(len(ciphertext) / num_cols)
    num_shaded_boxes = (num_cols * num_rows) - len(ciphertext)
    
    plaintext = [""] * num_cols
    col = 0
    row = 0
    
    for symbol in ciphertext:
        plaintext[col] += symbol
        row += 1
        if (row == num_rows) or (row == num_rows - 1 and col >= num_cols - num_shaded_boxes):
            col += 1
            row = 0
    return "".join(plaintext)

# Combined Custom Cipher
def custom_encrypt(plaintext, key):
    stage1 = vigenere_cipher(plaintext, key, encrypt=True)
    return transposition_encrypt(stage1, key)

def custom_decrypt(ciphertext, key):
    stage1 = transposition_decrypt(ciphertext, key)
    return vigenere_cipher(stage1, key, encrypt=False)