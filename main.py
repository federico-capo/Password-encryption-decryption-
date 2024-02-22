from tkinter import *
from tkinter import filedialog, simpledialog
from cryptography.fernet import Fernet
import os

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

#carica chiave
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

#bottone cifra file compreso di carica chiave
def cifra_file():
    file = filedialog.askopenfilename(title="Seleziona il file da cifrare")
    if os.path.exists(file):
        with open(file, 'rb') as f:
            data = f.read()
        key, key_filename = carica_chiave()
        cipher = Fernet(key)
        encrypted_data = cipher.encrypt(data)
        with open(file, 'wb') as f:
            f.write(encrypted_data)
        result_label.config(text="File cifrato con successo.")
    else:
        result_label.config(text="File non esistente.")

def decifra_file():
    file = filedialog.askopenfilename(title="Seleziona il file da decifrare")
    if os.path.exists(file):
        with open(file, 'rb') as f:
            data = f.read()
        key, key_filename = carica_chiave()
        cipher = Fernet(key)
        decrypted_data = cipher.decrypt(data)
        with open(file, 'wb') as f:
            f.write(decrypted_data)
        result_label.config(text="File decifrato con successo.")
    else:
        result_label.config(text="File non esistente.")

# GUI
root = Tk()
root.title("Cifratura/Decifratura File")
root.geometry("410x150")
root.configure(bg='#141212')

# Etichetta per il risultato
result_label = Label(root, text="", bg='#141212', fg='#ffffff',font=("Arial", 9,'bold') )
result_label.grid(row=4, column=0, columnspan=3)

# #genera chiave
btn_key = Button(root, text='Genera chiave', bd='6', command=genera_chiave,bg='blue', fg='#ffffff',font=("Arial", 9,'bold') )
btn_key.grid(row=0, column=2, pady=10, padx=1, ipadx=20)

# bottone decifra file
btn_cifra = Button(root, text='Decifra file', bd='6', command=decifra_file, bg='green', fg='#ffffff',font=("Arial", 9,'bold') )
btn_cifra.grid(row=0, column=0, pady=10, padx=10, ipadx=20)
# bottone cifra file
btn_cifra = Button(root, text='Cifra file', bd='6', command=cifra_file, bg='red', fg='#ffffff',font=("Arial", 9,'bold') )
btn_cifra.grid(row=0, column=1, pady=10, padx=10, ipadx=20)

# Bottone Esci
btn_exit = Button(root, text='Esci', bd='6', command=root.destroy)
btn_exit.grid(row=1, column=1, pady=10, padx=10, ipadx=20)


# Esegui la finestra
root.mainloop()
