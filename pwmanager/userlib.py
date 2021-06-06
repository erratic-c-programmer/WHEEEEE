#! /usr/bin/python3

import os
import hashlib
import random, string


def get_salt():
    return ''.join(random.choices(string.ascii_letters + string.digits, k=128))


def hash_passwd(plain, salt):
    """
    Salt and hash input password. Length 128.
    """
    return hashlib.pbkdf2_hmac('sha512', plain.encode(), salt.encode(), 100000, 64).hex() #?!?!


def hash_uname(plain):
    """
    Hash username into hash digest of length 128
    """
    return hashlib.sha512(plain.encode()).hexdigest()


######


class userfile:
    def __init__(self, passwdfilename, shadowfilename):
        self.pwfname = passwdfilename
        self.sfname = shadowfilename


    def __enter__(self):
        return self


    def add_user(self, username, passwd):
        with open(self.pwfname, "a") as pwfile, open(self.sfname, "a") as sfile:
            salt = get_salt()
            # Write the username and : delimeter
            # Fixed-length usernames of 128 characters
            pwfile.write(hash_uname(username)) # write hash
            pwfile.write(salt) # write salt
            sfile.write(hash_passwd(passwd, salt)) # write hash
            return


    def check(self, username, passwd):
        # Sanity
        if len(username) * len(passwd) == 0:
            return False

        # Init values
        storedas = 1
        with open(self.pwfname, "r") as pwfile, open(self.sfname, "r") as sfile:
            # If it's the first
            cur_read = pwfile.read(128 + 128)
            cur_uname = cur_read[:128]
            cur_salt = cur_read[128:]

            while(cur_uname != hash_uname(username)):
                storedas += 1
                cur_read = pwfile.read(128 + 128)
                if len(cur_read) == 0:
                    hash_passwd("hohoho", "teehee") # prevent timing attacks I guess?
                    return False
                cur_uname = cur_read[:128]
                cur_salt = cur_read[128:]

            hashed = hash_passwd(passwd, cur_salt)

            # Check against the true hash
            truehash = None
            for _ in range(storedas):
                truehash = sfile.read(128)

            return hashed == truehash
