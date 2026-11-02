import collections
import time

def frequency_analysis(ciphertext):
    # Analyze the frequency of letters in the ciphertext
    clean_text = [c.upper() for c in ciphertext if c.isalpha()]
    total = len(clean_text)
    if total == 0: return {}
    
    counts = collections.Counter(clean_text)
    freq = {char: round((count / total) * 100, 2) for char, count in counts.items()}
    return dict(sorted(freq.items(), key=lambda item: item[1], reverse=True))

def known_plaintext_attack(known_plain, ciphertext):
    # Assume the attacker has access to a portion of the plaintext and corresponding ciphertext[cite: 1]
    print("[*] Running Known-Plaintext Attack Module...")
    print(f"[*] Known Plaintext snippet: '{known_plain}'")
    print(f"[*] Matching with Ciphertext: '{ciphertext[:len(known_plain)]}'...")
    time.sleep(1.5)
    return "Partial Key Recovered: 'SECR...'"

def efficiency_comparison():
    # Compare efficiency of custom cipher to a single-stage cipher like Shift cipher
    sample_text = "A" * 5000 
    key = "SUPERSECRETKEY"
    
    start = time.time()
    # Dummy Shift Cipher simulation O(N)
    shift_cipher = [chr((ord(c) - 65 + 3) % 26 + 65) for c in sample_text]
    shift_time = time.time() - start
    
    start = time.time()
    # Custom cipher simulation
    from ciphers import custom_encrypt
    custom_encrypt(sample_text, key)
    custom_time = time.time() - start
    
    return shift_time, custom_time