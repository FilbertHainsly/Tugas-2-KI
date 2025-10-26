import socket
import threading
from DES import encrypt_buffer, decrypt_buffer

def receive_messages(sock, key):
    while True:
        try:
            data = sock.recv(8192)
            if not data:
                break
            ciphertext = data.decode('latin1')
            try:
                plaintext = decrypt_buffer(ciphertext, key)
                print(f"\n[Pesan Diterima]: {plaintext}")
            except Exception as e:
                print(f"\n[Error Dekripsi]: {e}")
        except:
            print("[Koneksi terputus]")
            break

if __name__ == "__main__":
    server_ip = input("Masukkan IP: ")
    server_port = int(input("Masukkan Port: "))
    key = input("Masukkan key DES (maks 8 karakter): ")

    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((server_ip, server_port))
    print(f"[TERHUBUNG] ke client 2 {server_ip}:{server_port}")

    threading.Thread(target=receive_messages, args=(sock, key), daemon=True).start()

    while True:
        msg = input("Ketik pesan: ")
        if msg.lower() == "exit":
            sock.close()
            print("Koneksi ditutup.")
            break

        ciphertext = encrypt_buffer(msg, key)
        sock.sendall(ciphertext.encode('latin1'))
