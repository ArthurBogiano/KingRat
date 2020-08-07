#!/bin/env python3

import socket
from threading import Thread
import random


# cria sockets
def init():
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    return sock


# adiciona threads de listen por porta
def addListen(sock, port):
    global threads
    try:
        id = random_id()
        tr = Thread(target=listen, args=(sock, port, id))
        print(f'[+] Listen na porta {port} iniciado')
        tr.start()
        threads.append((id, port, tr, sock))
    except:
        print('[-] Erro ao criar socket')


# o que cada listen executa
def listen(sock, port, tr_id):
    global sessions

    sock.bind(('0.0.0.0', port))
    sock.listen(100)

    while True:
        try:
            con, cli = sock.accept()
            whoami = con.recv(1024)
            sessions.append((con, cli, whoami.decode()))
            print(f'\n[+] Nova sessão criada na porta {port}')
        except:
            break

    print(f'\n[+] Finalizando listen na porta {port}')


# id alearoria, porem que não se repita para threads
def random_id():
    global random_list

    while True:
        id = random.randint(1, 1000)
        if not id in random_list:
            break

    random_list.append(id)
    return id


# desliga listen e remove thread
def killListen(id):
    global threads

    if id == 'all':
        print(f'[*] Matando listens')
        for tr in threads:
            tr[3].close()
            threads.remove(tr)
            return 0

    if not id.isnumeric():
        print(f'[-] Erro: O id deve ser númerico')
        return 0

    ok = False
    for tr in threads:
        if tr[0] == int(id):
            tr[3].close()
            threads.remove(tr)
            ok = True
            print(f'[+] Listen {id} morto')

    if not ok:
        listListens()


# lista portas em listen
def listListens():
    global threads

    print("======================")
    print("       Listens")
    print("======================")
    print(" ID | PORT")
    for l in threads:
        print(f'{l[0]} | {l[1]}')
    print("======================")


# lista portas em listen
def listSessions():
    global threads

    print("======================")
    print("       Sessions")
    print("======================")
    print(" ID | HOST | USER")
    for l in sessions:
        print(f'{sessions.index(l)} | {l[1][0]} | {l[2]}')
    print("======================")


#interage com uma sessão shell
def interact(id):
    global sessions

    if not id.isnumeric():
        print(f'[-] Erro: O id deve ser númerico')
        return 0

    id = int(id)

    sess = sessions[id]
    con = sess[0]

    try:
        while True:
            cmd = input(f'{sess[2]} ~# ')

            if cmd == '':
                continue

            if not cmd:
                continue

            if cmd == 'exit':
                break

            con.send(cmd.encode())
            while True:
                data = con.recv(1024)
                data = data.decode()
                print(data)
                if '[+] Executado' in data:
                    break

    except Exception as err:
        print(f'[-] Session error: {err}')
        con.close()
        sessions.remove(sess)
        pass


def help():
    print("\nComandos disponiveis:\n")

    str = 'listens : listens ativos\n' \
          'sessions : sessões ativas\n' \
          'kill : mata listens ou sessions\n' \
          'i : inicia interação com uma session\n'

    print(str)


# Função principal
if __name__ == '__main__':

    #threads
    random_list = []
    threads = []

    #sessions
    sessions = []

    print('[+] Iniciando listen')
    addListen(init(), 9090)

    while True:
        cmd = input('[?] Comando: ')

        if cmd == 'listens':
            listListens()

        if cmd == 'sessions':
            listSessions()

        if 'kill' in cmd:
            args = cmd.split(' ')

            if len(args) >= 2:
                if args[1] == '-s':
                    print(f'killing session {args[2]}')
                elif args[1] == '-l':
                    killListen(args[2] if len(args) == 3 else '')
                else:
                    print('Command "kill":\n -l : matar listens\n -s : matar sessions\n Exemple: kill -l 123')
            else:
                print('Usage: kill [type] [id]')

        if cmd == 'exit':
            killListen('all')
            exit('[+] Volte sempre :3')

        if 'i ' in cmd:
            args = cmd.split(' ')
            if len(args) == 2:
                interact(args[1])
            else:
                print('Command "i": i [session_id]')

        if cmd == 'help':
            help()