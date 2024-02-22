from tkinter import *
from tkinter import filedialog, simpledialog
from cryptography.fernet import Fernet
import os

def generate_key():
    return Fernet.generate_key()

def save_key(key, filename):
    with open(filename, 'wb') as key_file:
        print(f"Chiave salvata in '{filename}'")
        result_label.config(text=f"Chiave salvata in '{filename}'")
        key_file.write(key)

def load_key(filename):
    result_label.config(text="Chiave caricata con successo.")
    print("Chiave caricata con successo.")
    print(f"File chiave: {filename}")
    return open(filename, 'rb').read()

def get_key_choice():
    key_choice = simpledialog.askstring("Scelta chiave", "Vuoi generare una nuova chiave o utilizzare una già esistente? (si/no): ").lower()
    if key_choice == 'si':
        return generate_key(),
    elif key_choice == 'no':
        key_filename = filedialog.askopenfilename(title="Seleziona il file chiave")
        if os.path.exists(key_filename):
            return load_key(key_filename),
        else:
            print(f"Il file chiave '{key_filename}' non esiste. Generazione di una nuova chiave.")
            return generate_key(),
    else:
        print("Scelta non valida. Generazione di una nuova chiave.")
        return generate_key(),


def genera_chiave():
    chiave = Fernet.generate_key()
    result_label.config(text="Nuova chiave generata con successo.")
    print("Nuova chiave generata con successo.")
    print(f"Chiave: {chiave}")
    salva_chiave(chiave)
    return chiave
#salva chiave
def salva_chiave(chiave):
    with open('chiave.key', 'wb') as file_chiave:
        file_chiave.write(chiave)    

#carica chiave ma cambia nome file in chiave.key
def carica_chiave():
    file_chiave= "chiave.key"
    file_chiave = filedialog.askopenfilename(title="Seleziona il file chiave")
    if os.path.exists(file_chiave):
        result_label.config(text="Chiave caricata con successo.")
        print("Chiave caricata con successo.")
        print(f"File chiave: {file_chiave}")
        return open(file_chiave, 'rb').read(), file_chiave
    else:
        print(f"Il file chiave '{file_chiave}' non esiste. Generazione di una nuova chiave.")
        return genera_chiave()


def carica_chiave1():
    key_filename = filedialog.askopenfilename(title="Seleziona il file chiave")
    if os.path.exists(key_filename):
        return load_key(key_filename), key_filename
    else:
        print(f"Il file chiave '{key_filename}' non esiste. Generazione di una nuova chiave.")
        return generate_key(), None,


def encrypt_file(key, filename, output_filename, result_label):
    cipher = Fernet(key)
    with open(filename, 'rb') as file:
        data = file.read()
        encrypted_data = cipher.encrypt(data)
    with open(output_filename, 'wb') as file:
        file.write(encrypted_data)
    result_label.config(text="File cifrato con successo.")

def decrypt_file(key, filename, output_filename, result_label):
    cipher = Fernet(key)
    with open(filename, 'rb') as file:
        encrypted_data = file.read()
        decrypted_data = cipher.decrypt(encrypted_data)
    with open(output_filename, 'wb') as file:
        file.write(decrypted_data)
    result_label.config(text="File decifrato con successo.")

def main():
    key_filename = 'secret.key'
    key_result = get_key_choice()

    if len(key_result) == 2:
        key, existing_key_filename = key_result
        key_filename = existing_key_filename
    else:
        key, existing_key_filename = key_result[0], None
        save_key(key, key_filename)
        print("Chiave pronta.")

    action_choice = simpledialog.askstring("Scelta azione", "Vuoi cifrare o decifrare un file? (c/d): ").lower()

    if action_choice == 'c':
        input_filename = filedialog.askopenfilename(title="Seleziona il file da cifrare")
        output_filename = filedialog.asksaveasfilename(title="Seleziona il file cifrato di output")
        encrypt_file(key, input_filename, output_filename, result_label)
    elif action_choice == 'd':
        decrypt_filename = filedialog.askopenfilename(title="Seleziona il file da decifrare")
        decrypted_output_filename = filedialog.asksaveasfilename(title="Seleziona il file decifrato di output")
        decrypt_file(key, decrypt_filename, decrypted_output_filename, result_label)
    else:
        print("Scelta non valida.")

# GUI
root = Tk()
root.title("Cifratura/Decifratura File")
root.geometry("400x400")
root.configure(bg='#141212')

# Etichetta per il risultato
result_label = Label(root, text="", bg='#141212', fg='white')
result_label.grid(row=4, column=0, columnspan=3)

# Bottone Esegui
btn_run = Button(root, text='Esegui', bd='6', command=main)
btn_run.grid(row=0, column=0, pady=10, padx=10, ipadx=20)

#carica chiave
btn_key = Button(root, text='Carica chiave', bd='6', command=carica_chiave)
btn_key.grid(row=0, column=1, pady=10, padx=10, ipadx=20)
#genera chiave
btn_key = Button(root, text='Genera chiave', bd='6', command=genera_chiave)
btn_key.grid(row=1, column=1, pady=10, padx=10, ipadx=20)

# Bottone Esci
btn_exit = Button(root, text='Esci', bd='6', command=root.destroy)
btn_exit.grid(row=0, column=2, pady=10, padx=10, ipadx=20)

# Esegui la finestra
root.mainloop()
