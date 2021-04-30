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






# Signal handling
def int_sig_handle(sig, frame):
    print("???")

def term_sig_handle(sig, frame):
    print(":(")
    sys.exit(0)

signal.signal(signal.SIGINT, int_sig_handle)
signal.signal(signal.SIGTERM, term_sig_handle)






def childproc(conn, clientaddr):
    # the state machine
    uf = ul.userfile(PASSWDF, SHADOWF)
    iuname = conn.recv(1024)[:-2].decode()

    # THIS HACC
    if (iuname == "DIE IDIOT"):
        os.kill(os.getppid(), signal.SIGTERM)
        return

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
    try:
        while True:
            conn, addr = s.accept()
            newpid = os.fork()
            if newpid == 0:
                childproc(conn, addr)
            else:
                children.append(newpid)
    finally:
        # mercilessly slaughter all our children
        for c in children:
            os.kill(c, signal.SIGKILL)
            # reap zombie children
            os.waitpid(c, 0)
