#! /usr/bin/python3
from userlib import *

uname = input("Input new USERNAME > ")
passwd = input("Input new PASSWORD > ")
if input("Confirm new PASSWORD > ") != passwd:
    print("Passwords do not match!")
    exit(1)

u = userfile("passwd", "shadow")

u.add_user(uname, passwd)
