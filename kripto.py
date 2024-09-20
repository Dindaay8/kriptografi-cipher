import tkinter as tk
from tkinter import filedialog, messagebox

# Vigenere Cipher
def vigenere_encrypt(plaintext, key):
    result = ""
    key_length = len(key)
    key_int = [ord(i) - 65 for i in key.upper()]
    plaintext_int = [ord(i) - 65 for i in plaintext.upper() if i.isalpha()]

    for i in range(len(plaintext_int)):
        value = (plaintext_int[i] + key_int[i % key_length]) % 26
        result += chr(value + 65)
    return result

def vigenere_decrypt(ciphertext, key):
    result = ""
    key_length = len(key)
    key_int = [ord(i) - 65 for i in key.upper()]
    ciphertext_int = [ord(i) - 65 for i in ciphertext.upper() if i.isalpha()]

    for i in range(len(ciphertext_int)):
        value = (ciphertext_int[i] - key_int[i % key_length]) % 26
        result += chr(value + 65)
    return result

# Playfair Cipher
def create_playfair_matrix(key):
    key = ''.join(dict.fromkeys(key.upper().replace('J', 'I')))  # Remove duplicates and replace J with I
    alphabet = "ABCDEFGHIKLMNOPQRSTUVWXYZ"
    matrix = []

    for char in key:
        if char in alphabet and char not in matrix:
            matrix.append(char)

    for char in alphabet:
        if char not in matrix:
            matrix.append(char)

    return matrix  # Mengembalikan list 1D

def playfair_encrypt(plaintext, key):
    plaintext = ''.join([char.upper().replace('J', 'I') for char in plaintext if char.isalpha()])
    matrix = create_playfair_matrix(key)
    result = ""

    pairs = []
    i = 0
    while i < len(plaintext):
        a = plaintext[i]
        if i + 1 < len(plaintext):
            b = plaintext[i + 1]
            if a == b:
                pairs.append(a + 'X')
                i += 1
            else:
                pairs.append(a + b)
                i += 2
        else:
            pairs.append(a + 'X')
            i += 1

    for a, b in pairs:
        row_a, col_a = divmod(matrix.index(a), 5)
        row_b, col_b = divmod(matrix.index(b), 5)

        if row_a == row_b:  # Same row
            result += matrix[row_a * 5 + (col_a + 1) % 5]
            result += matrix[row_b * 5 + (col_b + 1) % 5]
        elif col_a == col_b:  # Same column
            result += matrix[((row_a + 1) % 5) * 5 + col_a]
            result += matrix[((row_b + 1) % 5) * 5 + col_b]
        else:  # Rectangle
            result += matrix[row_a * 5 + col_b]
            result += matrix[row_b * 5 + col_a]

    return result

def playfair_decrypt(ciphertext, key):
    matrix = create_playfair_matrix(key)
    result = ""
    ciphertext = ciphertext.upper().replace('J', 'I')

    pairs = []
    for i in range(0, len(ciphertext), 2):
        a = ciphertext[i]
        if i + 1 < len(ciphertext):
            b = ciphertext[i + 1]
            pairs.append((a, b))

    for a, b in pairs:
        row_a, col_a = divmod(matrix.index(a), 5)
        row_b, col_b = divmod(matrix.index(b), 5)

        if row_a == row_b:  # Same row
            result += matrix[row_a * 5 + (col_a - 1) % 5]
            result += matrix[row_b * 5 + (col_b - 1) % 5]
        elif col_a == col_b:  # Same column
            result += matrix[((row_a - 1) % 5) * 5 + col_a]
            result += matrix[((row_b - 1) % 5) * 5 + col_b]
        else:  # Rectangle
            result += matrix[row_a * 5 + col_b]
            result += matrix[row_b * 5 + col_a]

    return result

# Hill Cipher (Contoh sederhana dengan kunci tetap)
def hill_encrypt(plaintext, key):
    key_matrix = [[6, 24], [1, 13]]  # Contoh kunci 2x2
    result = ""
    plaintext = plaintext.upper().replace(' ', '').replace('J', 'I')
    
    for i in range(0, len(plaintext), 2):
        if i + 1 < len(plaintext):
            a = ord(plaintext[i]) - 65
            b = ord(plaintext[i + 1]) - 65
            c = (key_matrix[0][0] * a + key_matrix[0][1] * b) % 26
            d = (key_matrix[1][0] * a + key_matrix[1][1] * b) % 26
            result += chr(c + 65) + chr(d + 65)

    return result

def hill_decrypt(ciphertext, key):
    inverse_key_matrix = [[15, 17], [25, 7]]  # Kunci invers 2x2
    result = ""
    
    for i in range(0, len(ciphertext), 2):
        if i + 1 < len(ciphertext):
            a = ord(ciphertext[i]) - 65
            b = ord(ciphertext[i + 1]) - 65
            c = (inverse_key_matrix[0][0] * a + inverse_key_matrix[0][1] * b) % 26
            d = (inverse_key_matrix[1][0] * a + inverse_key_matrix[1][1] * b) % 26
            result += chr(c + 65) + chr(d + 65)

    return result

# Upload file and read content
def upload_file():
    file_path = filedialog.askopenfilename()
    with open(file_path, 'r') as file:
        content = file.read()
    input_text.delete(1.0, tk.END)
    input_text.insert(tk.END, content)

# Encrypt and decrypt based on selected cipher
def process_text():
    action = action_var.get()
    cipher = cipher_var.get()
    text = input_text.get("1.0", tk.END).strip()
    key = key_entry.get()
    
    if len(key) < 12:
        messagebox.showerror("Error", "Key must be at least 12 characters long.")
        return

    if action == "Encrypt":
        if cipher == "Vigenere":
            encrypted = vigenere_encrypt(text, key)
            output_text.delete(1.0, tk.END)
            output_text.insert(tk.END, encrypted)
        elif cipher == "Playfair":
            encrypted = playfair_encrypt(text, key)
            output_text.delete(1.0, tk.END)
            output_text.insert(tk.END, encrypted)
        elif cipher == "Hill":
            encrypted = hill_encrypt(text, key)  # Kunci tetap dalam contoh
            output_text.delete(1.0, tk.END)
            output_text.insert(tk.END, encrypted)
    elif action == "Decrypt":
        if cipher == "Vigenere":
            decrypted = vigenere_decrypt(text, key)
            output_text.delete(1.0, tk.END)
            output_text.insert(tk.END, decrypted)
        elif cipher == "Playfair":
            decrypted = playfair_decrypt(text, key)
            output_text.delete(1.0, tk.END)
            output_text.insert(tk.END, decrypted)
        elif cipher == "Hill":
            decrypted = hill_decrypt(text, key)  # Kunci tetap dalam contoh
            output_text.delete(1.0, tk.END)
            output_text.insert(tk.END, decrypted)

# Setup GUI
root = tk.Tk()
root.title("Cipher Program")

cipher_var = tk.StringVar(value="Vigenere")
action_var = tk.StringVar(value="Encrypt")

cipher_label = tk.Label(root, text="Select Cipher:")
cipher_label.pack()
vigenere_radio = tk.Radiobutton(root, text="Vigenere", variable=cipher_var, value="Vigenere")
playfair_radio = tk.Radiobutton(root, text="Playfair", variable=cipher_var, value="Playfair")
hill_radio = tk.Radiobutton(root, text="Hill", variable=cipher_var, value="Hill")
vigenere_radio.pack()
playfair_radio.pack()
hill_radio.pack()

action_label = tk.Label(root, text="Select Action:")
action_label.pack()
encrypt_radio = tk.Radiobutton(root, text="Encrypt", variable=action_var, value="Encrypt")
decrypt_radio = tk.Radiobutton(root, text="Decrypt", variable=action_var, value="Decrypt")
encrypt_radio.pack()
decrypt_radio.pack()

key_label = tk.Label(root, text="Enter Key (min 12 chars):")
key_label.pack()
key_entry = tk.Entry(root)
key_entry.pack()

upload_button = tk.Button(root, text="Upload Text File", command=upload_file)
upload_button.pack()

input_label = tk.Label(root, text="Input Text:")
input_label.pack()
input_text = tk.Text(root, height=10, width=50)
input_text.pack()

output_label = tk.Label(root, text="Output Text:")
output_label.pack()
output_text = tk.Text(root, height=10, width=50)
output_text.pack()

process_button = tk.Button(root, text="Process", command=process_text)
process_button.pack()

root.mainloop()
