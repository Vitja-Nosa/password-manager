from getpass import getpass
import json
from quopri import encodestring
from re import search
import string
import random
import os
from cryptocode import encrypt, decrypt
import pyperclip as pc
from os.path import exists
from hashlib import sha256 as hashValue

def saveKey(key):
    key_hashed = hashValue(str.encode(key)).hexdigest()
    f = open('masterkey', 'w')
    f.write(key_hashed)
    f.close()
    print('Key has been saved!')

def compareKey(key):
    key_hashed = hashValue(str.encode(key)).hexdigest()
    f = open('masterkey', 'r')
    l = f.readline()
    f.close() 
    return l == key_hashed

def getAllCredentials(key):
    f = open('credentials', 'r')
    l = f.readline()
    f.close()
    raw = decrypt(l, key)
    return json.loads(raw)

def createAccount(search_term, username, password, key):
    data = getAllCredentials(key)
    data[search_term] = {
        "username": username,
        "password": password
    }
    pc.copy(password)
    f = open('credentials', 'w')
    f.write(encrypt(json.dumps(data), key))
    f.close()
    del data
    print('Credentials have been saved and password has been coppied')

def importNewData(data, key):
    f = open('credentials', 'w')
    f.write(encrypt(json.dumps(data), key))
    f.close() 

def generatePassword(len):
    print('Generating password...')
    characters = string.ascii_letters + string.digits + string.punctuation
    password = ''
    for i in range(22):
        password += random.choice(characters)
    return password

def askSearchterm(key):
    os.system('cls')
    data = getAllCredentials(key)
    print('Add a search term for your credentials.\n')
    while True:
        cmd = input("search term: ")
        if cmd == '':
            os.system('cls')
            print('Your credentials need to have a search term. \nPlease type in your search term.\n')
        elif cmd == '!show':
            os.system('cls')
            print('This cannot be a search term because it is already a command. \nPlease use a different search term.\n')
        elif cmd in data:
            os.system('cls')
            print('The search term you wanna use already exists. \nPlease use a different search term.\n')
        else:
            del data
            return cmd

def askUsername():
    os.system('cls')
    print('Type in an username for your credentials. \nLeave blank if you dont want one for your account.\n')
    cmd = input('username: ')
    if cmd == '':
        return None
    else:
        return cmd

def askPassword():
    os.system('cls')
    print('Type in a password for your credentials. \nLeave blank if you want a password generated.\n')
    cmd = input('password: ')
    if cmd == '':
        return generatePassword(22)
    else:
        return cmd
    
def findSearchTerm():
    os.system('cls')
    show = False
    while True:
        print('Type an existing search term to find the matching credentials.')
        if not show:
            print('To see all existing search terms type "!show"')
        cmd = input(': ')
        show = False
        data = getAllCredentials(used_key)
        if cmd == '!show':
            show = True
            os.system('cls')
            for key in data.keys():
                print('- '+key)
            print('')
        elif cmd in data:
            os.system('cls')
            print('Search term found.\nWhat would you like to do?')
            del data
            return cmd
        else:
            os.system('cls')
            print('Search term not found.')

used_key = None

os.system('cls')
if exists("masterkey"):
    while True:
        print("Type in your master password (key).")
        key = getpass(': ')
        identical = compareKey(key)
        if identical:
            used_key = key
            os.system('cls')
            print('Welcome back.')
            break
        else:
            os.system('cls')
            print('Wrong password, try again.')
else:
    while True:
        print("Create a new master password (key).")
        key = getpass(": ")
        print("Re-enter master password.")
        key_confirm = getpass(": ")
        if key == key_confirm:
            used_key = key
            saveKey(key)
            f = open("credentials", "w")
            f.write(encrypt("{"+"}",used_key))
            f.close()
            os.system('cls')
            print('Key is saved, you are now logged in.')
            break
        else:
            os.system('cls')
            print('Passwords do not match.')

while True:
    print('+-----------------------+')
    print('| 1. Create credentials |')
    data = getAllCredentials(used_key)
    hasData = False
    if data:
        del data
        hasData = True
        print('| 2. Read credentials   |')
        print('| 3. Update credentials |')
        print('| 4. Delete credentials |')
    print('+-----------------------+')
    
    cmd = input(': ')
    if cmd == '1':
        search_term = askSearchterm(used_key)
        username = askUsername()
        password = askPassword()
        os.system('cls')
        createAccount(search_term, username, password, used_key)
    elif hasData:
        if cmd == '2':
            search_term = findSearchTerm()
            data = getAllCredentials(used_key)
            while True:
                print('+----------------------+')
                print('| 1. copy password     |')
                print('| 2. show password     |')
                if data[search_term]['username'] != None:
                    print('| 3. copy username     |')
                    print('| 4. show username     |')
                print('| 5. exit              |')
                print('+----------------------+')
                cmd = input(': ')
                os.system('cls')
                if cmd == '1':
                    pc.copy(data[search_term]['password'])
                    print('Password has been coppied to your clipboard.')
                elif cmd == '2':
                    print('Password: '+ data[search_term]['password'])
                elif cmd == '3' and data[search_term]['username'] != None:
                    pc.copy(data[search_term]['username'])
                    print('Username has been coppied to your clipboard.')
                elif cmd == '4' and data[search_term]['username'] != None:
                    print('Username: '+ data[search_term]['username'])
                elif cmd == '5':
                    print('Welcome back.')
                    break
                else:
                    print('Unknown command, please use one of the following:')
            del search_term
            del data
        elif cmd == "3":
            search_term = findSearchTerm()
            data = getAllCredentials(used_key)
            while True:
                print('+-------------------------+')
                print('| 1. change search term   |')
                if data[search_term]['username'] != None:
                    print('| 2. change username      |')
                else:
                    print('| 2. add username         |')
                print('| 3. change password      |')
                print('| 4. exit                 |')
                print('+-------------------------+')
                cmd = input(': ')
                if cmd == '1':
                    old_search_term = search_term
                    new_search_term = askSearchterm(used_key)
                    os.system('cls')
                    print('Please type in your master password to change your credentials.')
                    while True:
                        key = getpass(': ')
                        if compareKey(key):
                            search_term = new_search_term
                            data[search_term] = data.pop(old_search_term)
                            importNewData(data, used_key)
                            os.system('cls')
                            print('Credentials have been updated.')
                            break
                        else:
                            os.system('cls')
                            print('Wrong password, try again.')
                elif cmd == '2':
                    username = askUsername()
                    os.system('cls')
                    print('Please type in your master password to change your credentials.')
                    while True:
                        key = getpass(': ')
                        if compareKey(key):
                            data[search_term]['username'] = username
                            importNewData(data, used_key)
                            os.system('cls')
                            print('Credentials have been updated.')
                            break
                        else:
                            os.system('cls')
                            print('Wrong password, try again.')
                elif cmd == '3':
                    password = askPassword()
                    os.system('cls')
                    print('Please type in your master password to change your credentials.')
                    while True:
                        key = input(": ")
                        if compareKey(key):
                            data[search_term]['password'] = password
                            importNewData(data, used_key)
                            os.system('cls')
                            print('Credentials have been updated.')
                            break
                        else:
                            os.system('cls')
                            print('Wrong password, try again.')
                elif cmd == '4':
                    os.system('cls')
                    print('Welcome back.')
                    break
                else:
                    os.system('cls')
                    print('Unknown command, please choose one of the following.')
            del search_term
            del data
        elif cmd == "4":
            search_term = findSearchTerm()
            data = getAllCredentials(used_key)
            os.system('cls')
            while True:
                print('Please confirm your master password to delete your credentials.')
                key = getpass(': ')
                if compareKey(key):
                    del data[search_term]
                    importNewData(data, used_key)
                    os.system('cls')
                    print(search_term+' has been removed.')
                    break
                else:
                    os.system('cls')
                    print('Wrong password, try again.')
            del search_term
            del data
        else:
            os.system('cls')
            print('Unknown command, please choose one of the following.')
    else:
        os.system('cls')
        print('Unknown command, please choose one of the following.')