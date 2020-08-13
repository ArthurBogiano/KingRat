from cryptography.fernet import Fernet
import os

print("[+] Gerando key")
key = Fernet.generate_key()

print("[+] Salvando key")
keytxt = open('hack.key', 'wb')
keytxt.write(key)
keytxt.close()
print(f"[+] key salva em {os.getcwd()}\\hack.key")

cipher_suite = Fernet(key)

print("[+] Lendo payload.txt")
txt = open('payload.txt', 'rb')
print("[+] Codificando payload")
cipher_text = cipher_suite.encrypt(txt.read())
txt.close()

print("[+] Salvando payload codificada")
txt2 = open('payload_encrypt.txt', 'wb')
txt2.write(cipher_text)
txt2.close()
print(f"[+] payload codificada salva em {os.getcwd()}\\payload_encrypt.txt")
