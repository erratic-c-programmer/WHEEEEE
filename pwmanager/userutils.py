import os
import hashlib


def hash_passwd(plain):
    '''
    Salt and hash input password.
    '''

    salt = os.urandom(32)
    hashed = hashlib.pbkdf2_hmac('sha512', plain.encode(),
                                 salt, 100000, 32)
    return hashed, salt


def hash_uname(plain):
    '''
    Hash username into checksum of length 128
    '''

    return hashlib.sha512(plain.encode()).hexdigest()
