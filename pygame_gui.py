import pygame
import sys
import os
import math  # Zoom aur pan ki calculations ke liye add kiya hai

from ciphers import custom_encrypt, custom_decrypt
from hacks import frequency_analysis

pygame.init()
pygame.mixer.init()

WIDTH, HEIGHT = 900, 650
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Ministry of Intelligence - Secure Terminal")

GREEN = (0, 255, 0)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 50, 50)

font = pygame.font.SysFont("courier", 18, bold=True)
font_large = pygame.font.SysFont("courier", 22, bold=True)

# 1. Background Image Load (Original image ko memory mein save rakha hai)
try:
    original_bg = pygame.image.load("map_bg.jpg").convert()
    original_bg = pygame.transform.smoothscale(original_bg, (WIDTH, HEIGHT))
except:
    original_bg = pygame.Surface((WIDTH, HEIGHT))
    original_bg.fill(BLACK)

# 2. Audio Setup (BGM, Main Voiceover, Encrypt/Decrypt Voices)
try:
    pygame.mixer.music.load("bg_music.mp3")
    pygame.mixer.music.set_volume(0.3)
    pygame.mixer.music.play(-1)
except:
    print("Background music file nahi mili.")

voice_channel = None
voice_finished = False
try:
    voice_sound = pygame.mixer.Sound("voiceover.mp3")
    voice_channel = voice_sound.play()
except:
    print("Voiceover file nahi mili.")
    voice_finished = True

# Nayi Encrypt / Decrypt Sounds load kar rahe hain
try:
    encrypt_sound = pygame.mixer.Sound("encrypt_success.mp3")
except:
    encrypt_sound = None

try:
    decrypt_sound = pygame.mixer.Sound("decrypt_success.mp3")
except:
    decrypt_sound = None

active_input = None 
input_message = ""
input_key = ""
output_text = "Voiceover briefing in progress... Please wait."
current_mode = "MENU" 

def draw_text(text, x, y, color=GREEN, lg=False):
    f = font_large if lg else font
    text_surface = f.render(text, True, color)
    screen.blit(text_surface, (x, y))

def main_loop():
    global voice_finished, output_text, input_message, input_key, current_mode, active_input
    running = True
    
    while running:
        # Time calculate kar rahe hain zoom/pan effect ke liye
        time_sec = pygame.time.get_ticks() / 1000.0
        
        if not voice_finished and voice_channel:
            if not voice_channel.get_busy():
                voice_finished = True
                output_text = "Briefing complete. System unlocked. Press [1] Encrypt or [2] Decrypt."

        # --- ANIMATED BACKGROUND LOGIC ---
        # Zoom scale 1.0 (normal) se 1.3 (zoomed) ke darmiyan smoothly change hoga
        zoom_factor = 1.0 + 0.3 * ((math.sin(time_sec * 0.2) + 1) / 2)
        
        new_w = int(WIDTH * zoom_factor)
        new_h = int(HEIGHT * zoom_factor)
        
        # Image ko scale karein
        animated_bg = pygame.transform.scale(original_bg, (new_w, new_h))
        
        # Pan coordinates calculate karein (Image bounds ke andar hi rehna chahiye)
        max_offset_x = new_w - WIDTH
        max_offset_y = new_h - HEIGHT
        
        # Cosine aur Sine ki madad se X aur Y axis par smooth panning
        offset_x = -int(max_offset_x * ((math.cos(time_sec * 0.3) + 1) / 2))
        offset_y = -int(max_offset_y * ((math.sin(time_sec * 0.4) + 1) / 2))
        
        screen.blit(animated_bg, (offset_x, offset_y))
        # ---------------------------------
        
        s = pygame.Surface((WIDTH, 260))
        s.set_alpha(230)
        s.fill(BLACK)
        screen.blit(s, (0, HEIGHT - 260))
        
        draw_text("MINISTRY OF INTELLIGENCE - SECURE TERMINAL", 20, HEIGHT - 250, WHITE, lg=True)
        
        if not voice_finished:
            draw_text("STATUS: Playing Intelligence Briefing (Please Listen)...", 20, HEIGHT - 210, RED)
            draw_text(output_text, 20, HEIGHT - 160, GREEN)
        else:
            if current_mode == "MENU":
                draw_text("STATUS: System Active & Unlocked", 20, HEIGHT - 210, GREEN)
                draw_text("Press [1] Encrypt Intel  |  [2] Decrypt Intel  |  [Q] Quit", 20, HEIGHT - 170, WHITE)
                draw_text(f"Result / Info: {output_text}", 20, HEIGHT - 120, GREEN)
            
            elif current_mode in ["ENCRYPT", "DECRYPT"]:
                draw_text(f"MODE: {current_mode} INTEL (Type below, Press ENTER to process, ESC to back)", 20, HEIGHT - 210, WHITE)
                
                msg_color = GREEN if active_input == 'message' else WHITE
                
                # Mode ke hisaab se label change hoga
                input_label = "Plaintext" if current_mode == "ENCRYPT" else "Ciphertext"
                draw_text(f"{input_label}: {input_message}_", 20, HEIGHT - 170, msg_color)
                
                key_color = GREEN if active_input == 'key' else WHITE
                draw_text(f"Key (Min 10 chars): {input_key}_", 20, HEIGHT - 130, key_color)
                
                draw_text(f"Output: {output_text}", 20, HEIGHT - 80, GREEN)

        pygame.display.flip()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q and current_mode == "MENU" and voice_finished:
                    running = False
                
                if voice_finished:
                    if current_mode == "MENU":
                        if event.key == pygame.K_1:
                            current_mode = "ENCRYPT"
                            input_message = ""
                            input_key = ""
                            output_text = "Enter message and key, then press Enter."
                            active_input = 'message'
                        elif event.key == pygame.K_2:
                            current_mode = "DECRYPT"
                            input_message = ""
                            input_key = ""
                            output_text = "Enter ciphertext and key, then press Enter."
                            active_input = 'message'
                            
                    elif current_mode in ["ENCRYPT", "DECRYPT"]:
                        if event.key == pygame.K_ESCAPE:
                            current_mode = "MENU"
                            output_text = "Returned to main menu."
                        elif event.key == pygame.K_TAB:
                            active_input = 'key' if active_input == 'message' else 'message'
                        elif event.key == pygame.K_RETURN:
                            if len(input_key) < 10:
                                output_text = "ERROR: Key must be at least 10 characters!"
                            else:
                                if current_mode == "ENCRYPT":
                                    res = custom_encrypt(input_message, input_key)
                                    output_text = f"Cipher: {res}"
                                    if encrypt_sound:
                                        encrypt_sound.play() # Play Encryption Success Sound
                                else:
                                    res = custom_decrypt(input_message, input_key)
                                    output_text = f"Plain: {res}"
                                    if decrypt_sound:
                                        decrypt_sound.play() # Play Decryption Success Sound
                        elif event.key == pygame.K_BACKSPACE:
                            if active_input == 'message':
                                input_message = input_message[:-1]
                            else:
                                input_key = input_key[:-1]
                        else:
                            if event.unicode.isprintable():
                                if active_input == 'message':
                                    input_message += event.unicode
                                elif active_input == 'key':
                                    input_key += event.unicode

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main_loop()