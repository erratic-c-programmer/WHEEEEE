#! /usr/bin/python
import os
import socket
import sys
import signal
sys.path.append("pwmanager")
import userlib as ul

HOST = "127.0.0.1"
PORT = int(sys.argv[1])
PASSWDF = "pwmanager/passwd"
SHADOWF = "pwmanager/shadow"










def childproc(conn, clientaddr):
    # the state machine
    uf = ul.userfile(PASSWDF, SHADOWF)
    iuname = conn.recv(1024)[:-2].decode()

    ipasswd = conn.recv(1024)[:-2].decode()

    if uf.check(iuname, ipasswd):
        conn.send("AOK".encode())
    else:
        conn.send("013".encode())
        conn.close()




    os._exit(0)







with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((HOST, PORT))
    s.listen()
    children = []
    while True:
        conn, addr = s.accept()
        newpid = os.fork()
        if newpid == 0:
            childproc(conn, addr)
        else:
            children.append(newpid)
