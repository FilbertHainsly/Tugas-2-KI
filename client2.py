import socket
from DES import encrypt_buffer, decrypt_buffer, pad_text

ip = input("Masukkan IP: ")
port = int(input("Masukkan Port: "))
key = input("Masukkan key DES (maks 8 karakter): ")
key = pad_text(key)[:8]

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((ip, port))
server.listen(1)
print(f"[LISTENING] koneksi berjalan di {ip}:{port}")

conn, addr = server.accept()
print(f"[CONNECTED] {addr}")

while True:
    data = conn.recv(1024)
    if not data:
        break

    ciphertext = data.decode("latin1")
    print(f"[RECEIVED] ({len(ciphertext)} bytes): {repr(ciphertext)}")

    plaintext = decrypt_buffer(ciphertext, key)
    print(f"[DECRYPTED] {plaintext}")
    
    reply = encrypt_buffer(f"Server terima: {plaintext}", key)
    conn.send(reply.encode("latin1"))

conn.close()
