#! /usr/bin/python3

import os

import userutils
import hashlib


class userfile:
    def __init__(self, passwdfilename, shadowfilename):
        self.passwdfile = open(passwdfilename, 'ab+')
        self.shadowfile = open(shadowfilename, 'ab+')

    def closestuff(self):
        self.passwdfile.close()
        self.shadowfile.close()


    def __enter__(self):
        return self


    def add_user(self, username, passwd):
        ret = userutils.hash_passwd(passwd)
        # Write the username and : delimeter
        # Fixed-length usernames of 128 characters
        self.passwdfile.write((userutils.hash_uname(username) + ':').encode('utf-8'))  # Write the hash
        self.passwdfile.write(ret[1])  # Write the salt
        # Write the hash
        self.shadowfile.write(ret[0])
        return


    def check(self, username, passwd):
        # Sanity
        if len(username) * len(passwd) == 0:
            return False

        # Init values
        storedas = 1
        # If it's the first
        self.passwdfile.seek(0)
        cur_read = self.passwdfile.read(128 + 1 + 32).split(':'.encode())
        cur_uname = cur_read[0]
        salt = cur_read[1]

        try:
            while(cur_uname.decode() != hashlib.sha512(username.encode()).hexdigest()):
                storedas += 1
                cur_read = self.passwdfile.read(128 + 1 + 32).split(':'.encode())
                cur_uname = cur_read[0]
                salt = cur_read[1]
        except IndexError:
            return False

        hashed = hashlib.pbkdf2_hmac('sha512', passwd.encode(),
                salt, 100000, 32)

        # Check against the true hash
        truehash = None
        self.shadowfile.seek(0)
        for _ in range(storedas):
            truehash = self.shadowfile.read(32)

        return hashed == truehash
