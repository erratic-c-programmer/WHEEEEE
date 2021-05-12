#! /usr/bin/python3
from userlib import *

uname = input('USERNAME > ')
passwd = input('PASSWORD > ')

if userfile("passwd", "shadow").check(uname, passwd):
    print('Logged in successfully.')

else:
    print('Authentication failure.')
