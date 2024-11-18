import math
from Crypto.Cipher import DES
from Crypto.Util.Padding import pad, unpad

def vigenere_encrypt(plaintext, key):
    plaintext = plaintext.replace(" ", "").upper()
    key = key.upper()
    key = (key * (len(plaintext) // len(key))) + key[:len(plaintext) % len(key)]
    ciphertext = ''
    print("\nАлфавит с индексами:")
    alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    for i, char in enumerate(alphabet):
        print(f"{char}({i})", end=" ")
    print("\n")
    for i in range(len(plaintext)):
        p = ord(plaintext[i]) - ord('A')
        k = ord(key[i]) - ord('A')
        c = (p + k) % 26
        ciphertext += chr(c + ord('A'))
    return ciphertext

def vigenere_decrypt(ciphertext, key):
    ciphertext = ciphertext.upper()
    key = key.upper()
    key = (key * (len(ciphertext) // len(key))) + key[:len(ciphertext) % len(key)]
    plaintext = ''
    for i in range(len(ciphertext)):
        c = ord(ciphertext[i]) - ord('A')
        k = ord(key[i]) - ord('A')
        p = (c - k) % 26
        plaintext += chr(p + ord('A'))
    return plaintext

def permute_encrypt(text):
    text = text.replace(" ", "")
    text_length = len(text)
    rows = math.floor(math.sqrt(text_length))
    cols = math.ceil(text_length / rows)
    if rows * cols < text_length:
        rows += 1
    text += ' ' * (rows * cols - text_length)
    matrix = [['' for _ in range(cols)] for _ in range(rows)]
    index = 0
    for j in range(cols):
        for i in range(rows):
            matrix[i][j] = text[index]
            index += 1
    print("Матрица для метода перестановки (по столбцам):")
    for row in matrix:
        print(" ".join(row))
    ciphertext = ''
    for i in range(rows):
        for j in range(cols):
            ciphertext += matrix[i][j]
    return ciphertext, rows, cols

def permute_decrypt(ciphertext, rows, cols):
    matrix = [['' for _ in range(cols)] for _ in range(rows)]
    index = 0
    for i in range(rows):
        for j in range(cols):
            if index < len(ciphertext):
                matrix[i][j] = ciphertext[index]
                index += 1
    plaintext = ''
    for j in range(cols):
        for i in range(rows):
            if matrix[i][j] != ' ':
                plaintext += matrix[i][j]
    return plaintext.strip()

def des_encrypt(plaintext, key):
    key = key.ljust(8, '0')[:8]
    cipher = DES.new(key.encode('utf-8'), DES.MODE_CBC, iv=b'12345678')
    padded_text = pad(plaintext.encode('utf-8'), DES.block_size)
    ciphertext = cipher.encrypt(padded_text)
    return ciphertext.hex()

def des_decrypt(ciphertext, key):
    key = key.ljust(8, '0')[:8]
    cipher = DES.new(key.encode('utf-8'), DES.MODE_CBC, iv=b'12345678')
    ciphertext_bytes = bytes.fromhex(ciphertext)
    decrypted_text = unpad(cipher.decrypt(ciphertext_bytes), DES.block_size).decode('utf-8')
    return decrypted_text

def main():
    while True:
        print("\nВыберите метод шифрования:")
        print("1. Метод Виженера")
        print("2. Метод перестановки")
        print("3. Алгоритм DES")
        print("0. Выход")
        choice = input("Введите номер метода: ")
        if choice == '0':
            print("Выход из программы.")
            break
        text = input("Введите текст для шифрования: ")
        if choice == '1':
            key = input("Введите ключ для Виженера: ")
            ciphertext = vigenere_encrypt(text, key)
            print(f"Зашифрованный текст: {ciphertext}")
            decrypted_text = vigenere_decrypt(ciphertext, key)
            print(f"Расшифрованный текст: {decrypted_text}")
        elif choice == '2':
            ciphertext, rows, cols = permute_encrypt(text)
            print(f"Зашифрованный текст: {ciphertext}")
            decrypted_text = permute_decrypt(ciphertext, rows, cols)
            print(f"Расшифрованный текст: {decrypted_text}")
        elif choice == '3':
            key_des = input("Введите ключ для DES (до 8 символов, будет дополнен автоматически): ")
            encrypted_text_des = des_encrypt(text, key_des)
            print(f"Зашифрованный текст (DES): {encrypted_text_des}")
            decrypted_text_des = des_decrypt(encrypted_text_des, key_des)
            print(f"Расшифрованный текст (DES): {decrypted_text_des}")
        else:
            print("Некорректный выбор метода. Попробуйте снова.")

if __name__ == "__main__":
    main()
