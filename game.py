import time
import os
import sys

# Aapki doosri files se functions import kar rahe hain
from ciphers import custom_encrypt, custom_decrypt
from hacks import frequency_analysis, known_plaintext_attack

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def type_writer(text, delay=0.03):
    for char in text:
        sys.stdout.write(char)
        sys.stdout.flush()
        time.sleep(delay)
    print()

def main_menu():
    while True:
        clear_screen()
        print("="*40)
        print("       MINISTRY OF INTELLIGENCE")
        print("          DATABASE ONE ACCESS")
        print("="*40)
        print("1. Encrypt Intel (Stage 1 & 2)")
        print("2. Decrypt Intel")
        print("3. Analyze Intercepted Data (Frequency)")
        print("4. Execute Known-Plaintext Attack")
        print("5. Exit")
        print("="*40)
        
        choice = input("Select an operation: ")
        
        if choice == '1':
            encrypt_interface()
        elif choice == '2':
            decrypt_interface()
        elif choice == '3':
            analyze_interface()
        elif choice == '4':
            attack_interface()
        elif choice == '5':
            type_writer("Logging out... MININT Agent out.")
            break
        else:
            print("Invalid selection.")
            time.sleep(1)

def encrypt_interface():
    clear_screen()
    type_writer("--- ENCRYPTING INTEL ---")
    plaintext = input("Enter transmission data: ")
    key = input("Enter encryption key (Min 10 chars): ")
    
    if len(key) < 10:
        type_writer("[!] Error: Key must be at least 10 characters.")
    else:
        type_writer("[*] Processing Multi-Stage Encryption...")
        ciphertext = custom_encrypt(plaintext, key)
        type_writer(f"[+] SUCCESS. CIPHERTEXT: {ciphertext}")
    input("\nPress Enter to return...")

def decrypt_interface():
    clear_screen()
    type_writer("--- DECRYPTING INTEL ---")
    ciphertext = input("Enter ciphertext to decrypt: ")
    key = input("Enter decryption key: ")
    
    type_writer("[*] Decrypting...")
    plaintext = custom_decrypt(ciphertext, key)
    type_writer(f"[+] SUCCESS. PLAINTEXT: {plaintext}")
    input("\nPress Enter to return...")

def analyze_interface():
    clear_screen()
    type_writer("--- FREQUENCY ANALYSIS ATTACK ---")
    ciphertext = input("Enter intercepted ciphertext: ")
    
    type_writer("[*] Analyzing Letter Distribution...")
    freq_data = frequency_analysis(ciphertext)
    
    for char, pct in list(freq_data.items())[:10]:
        print(f" - {char}: {pct}%")
    type_writer("[!] Note: Standard English 'E' frequency is ~12.7%. Flat distribution indicates a strong cipher.")
    input("\nPress Enter to return...")
    
def attack_interface():
    clear_screen()
    type_writer("--- KNOWN-PLAINTEXT ATTACK (KPA) ---")
    ciphertext = input("Enter full intercepted ciphertext: ")
    known_plain = input("Enter known portion of plaintext (e.g., 'ENEMY'): ")
    
    result = known_plaintext_attack(known_plain, ciphertext)
    type_writer(f"[+] RESULT: {result}")
    input("\nPress Enter to return...")

if __name__ == "__main__":
    main_menu()