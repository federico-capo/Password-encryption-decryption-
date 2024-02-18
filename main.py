from cryptography.fernet import Fernet
import os
import tkinter as tk
from tkinter import filedialog, simpledialog

def generate_key():
    return Fernet.generate_key()

def save_key(key, filename):
    with open(filename, 'wb') as key_file:
        key_file.write(key)

def load_key(filename):
    return open(filename, 'rb').read()

def get_key_choice():
    root = tk.Tk()
    root.withdraw()

    key_choice = tk.simpledialog.askstring("Scelta chiave", "Vuoi generare una nuova chiave o utilizzare una già esistente? (si/no): ").lower()
    if key_choice == 'si':
        return generate_key()
    elif key_choice == 'no':
        key_filename = filedialog.askopenfilename(title="Seleziona il file chiave")
        if os.path.exists(key_filename):
            return load_key(key_filename), key_filename  # Ritorna anche il percorso del file chiave
        else:
            print(f"Il file chiave '{key_filename}' non esiste. Generazione di una nuova chiave.")
            return generate_key(), None
    else:
        print("Scelta non valida. Generazione di una nuova chiave.")
        return generate_key(), None

def encrypt_file(key, filename, output_filename):
    cipher = Fernet(key)
    with open(filename, 'rb') as file:
        data = file.read()
        encrypted_data = cipher.encrypt(data)
    with open(output_filename, 'wb') as file:
        file.write(encrypted_data)

def decrypt_file(key, filename, output_filename):
    cipher = Fernet(key)
    with open(filename, 'rb') as file:
        encrypted_data = file.read()
        decrypted_data = cipher.decrypt(encrypted_data)
    with open(output_filename, 'wb') as file:
        file.write(decrypted_data)

def main():
    key_filename = 'secret.key'
    key, existing_key_filename = get_key_choice()

    if existing_key_filename is not None:
        # Se è stata scelta una chiave esistente, non chiedere il percorso di salvataggio
        key_filename = existing_key_filename
    else:
        save_key(key, key_filename)
        print("Chiave pronta.")

    root = tk.Tk()
    root.withdraw()

    action_choice = tk.simpledialog.askstring("Scelta azione", "Vuoi cifrare o decifrare un file? (c/d): ").lower()

    if action_choice == 'c':
        input_filename = filedialog.askopenfilename(title="Seleziona il file da cifrare")
        output_filename = filedialog.asksaveasfilename(title="Seleziona il file cifrato di output")
        encrypt_file(key, input_filename, output_filename)
        print("File cifrato con successo.")
    elif action_choice == 'd':
        decrypt_filename = filedialog.askopenfilename(title="Seleziona il file da decifrare")
        decrypted_output_filename = filedialog.asksaveasfilename(title="Seleziona il file decifrato di output")
        decrypt_file(key, decrypt_filename, decrypted_output_filename)
        print("File decifrato con successo.")
    else:
        print("Scelta non valida.")

if __name__ == "__main__":
    main()
