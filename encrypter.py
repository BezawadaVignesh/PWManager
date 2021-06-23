from Crypto.Cipher import AES
from Crypto.Hash import SHA256
from Crypto import Random
from cryptography.fernet import Fernet

import base64
import random

DEBUG=False

from hashlib import md5


def derive_key_and_iv(password, salt, key_length, iv_length):
    d = d_i = ''
    while len(d) < key_length + iv_length:
        d_i = md5(d_i + password + salt).digest()
        d += d_i
    return d[:key_length], d[key_length:key_length+iv_length]

# This encryption mode is no longer secure by today's standards.
# See note in original question above.
def obsolete_encrypt(in_file, out_file, password, key_length=32):
    bs = AES.block_size
    salt = Random.new().read(bs - len('Salted__'))
    key, iv = derive_key_and_iv(password, salt, key_length, bs)
    cipher = AES.new(key, AES.MODE_CBC, iv)
    out_file.write('Salted__' + salt)
    finished = False
    while not finished:
        chunk = in_file.read(1024 * bs)
        if len(chunk) == 0 or len(chunk) % bs != 0:
            padding_length = bs - (len(chunk) % bs)
            chunk += padding_length * chr(padding_length)
            finished = True
        out_file.write(cipher.encrypt(chunk))

def decrypt(in_file, out_file, password, key_length=32):
    bs = AES.block_size
    salt = in_file.read(bs)[len('Salted__'):]
    key, iv = derive_key_and_iv(password, salt, key_length, bs)
    cipher = AES.new(key, AES.MODE_CBC, iv)
    next_chunk = ''
    finished = False
    while not finished:
        chunk, next_chunk = next_chunk, cipher.decrypt(in_file.read(1024 * bs))
        if len(next_chunk) == 0:
            padding_length = ord(chunk[-1])
            if padding_length < 1 or padding_length > bs:
               raise ValueError("bad decrypt pad (%d)" % padding_length)
            # all the pad-bytes must be the same
            if chunk[-padding_length:] != (padding_length * chr(padding_length)):
               # this is similar to the bad decrypt:evp_enc.c from openssl program
               raise ValueError("bad decrypt")
            chunk = chunk[:-padding_length]
            finished = True
        out_file.write(chunk)

def encrypt(key, source, encode=True):
    key, source = key.encode(), source.encode()
    key = SHA256.new(key).digest() 
    IV = Random.new().read(AES.block_size)  
    encryptor = AES.new(key, AES.MODE_CBC, IV)
    padding = AES.block_size - len(source) % AES.block_size  
    source +=  bytes([padding]) * padding 
    data = IV + encryptor.encrypt(source)
    return base64.b64encode(data).decode() if encode else data

def decrypt(key, source, decode=True):
    if DEBUG==True:
        print("Key: ", key, "\nsource: ", source)
    if decode:
        source = base64.b64decode(source.encode())
    key = SHA256.new(key).digest()  
    IV = source[:AES.block_size]  
    decryptor = AES.new(key, AES.MODE_CBC, IV)
    data = decryptor.decrypt(source[AES.block_size:]) 
    padding = data[-1]  
    if data[-padding:] != bytes([padding]) * padding:  
        raise ValueError("Invalid padding...")
    return data[:-padding].decode('UTF-8')  

def make_password(plaintext, app_name):
    salt = get_hexdigest(plaintext, app_name)[:20]
    hsh = get_hexdigest(salt, plaintext)
    return ''.join((salt, hsh))

def get_hexdigest(salt, plaintext):
    return SHA256.new((salt + plaintext).encode('utf-8')).digest().hex()

def password(plaintext, app_name, length=16):
    raw_hex = make_password(plaintext, app_name)
    ALPHABET = ('abcdefghijklmnopqrstuvwxyz', 'ABCDEFGHIJKLMNOPQRSTYVWXYZ', '0123456789', '(/|!@#$%&)+=')
    
    pssword = ""
    num = random.randint(0, len(raw_hex)-length//2)
    raw_hex = raw_hex[num: num+length//2]
    while len(pssword) < length:
        if len(pssword) == (length//2)-1:
            pssword +=raw_hex
        n = random.randint(0, len(ALPHABET)-1)
        alpha = ALPHABET[n]
        n = random.randint(0, len(alpha)-1)
        pssword += alpha[n]

    return pssword
    
def run(commands):
    commands = ["store", "create", "find", "change", "delete"]


if __name__ == "__main__":
    '''
    try:
        commands = ["store", "create", "find", "change", "delete"]
        while True:
            request = input("> ")
            if request == "\q":
                print("Closeing shell..\n")
                break
            else:
                bad = True
                ucommands = request.split(" ")
                for command in commands:
                    for ucommand in ucommands:
                        if command == ucommand:
                            bad = False  
                            run(request)
                if bad:
                    print("I don't know that.")

    

    

        #print(decrypt(key="5e79bacad0f958956600511db76cf1af14a17e9f02d79a5b57a481b5fca46350".encode(), source="w4Qq3tLgX3vec/aeiXR/ffEXlypDxBpIiqsxoENwlIs="))
        #print(decrypt(key="f1af14a17e9f02d79a5b57a481b5fca46350".encode(), source="w4Qq3tLgX3vec/aeiXR/ffEXlypDxBpIiqsxoENwlIs="))
    except Exception as e:
        print("this -->",e)'''

class Encryptor():

    def key_create(self):
        key = Fernet.generate_key()
        return key

    def key_write(self, key, key_name):
        with open(key_name, 'wb') as mykey:
            mykey.write(key)

    def key_load(self, key_name):
        with open(key_name, 'rb') as mykey:
            key = mykey.read()
        return key


    def file_encrypt(self, key, original_file, encrypted_file):
        
        f = Fernet(key)

        with open(original_file, 'rb') as file:
            original = file.read()

        encrypted = f.encrypt(original)

        with open (encrypted_file, 'wb') as file:
            file.write(encrypted)

    def file_decrypt(self, key, encrypted_file, decrypted_file):
        
        f = Fernet(key)

        with open(encrypted_file, 'rb') as file:
            encrypted = file.read()

        decrypted = f.decrypt(encrypted)

        with open(decrypted_file, 'wb') as file:
            file.write(decrypted)
