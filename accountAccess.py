import mysql.connector
import random
import time
from hashlib import sha256 as userHash
from tryAction import tryAction

def hashSalt(password, salt):
    saltedPassword = password + str(salt)
    hasher = userHash(saltedPassword.encode('utf-8'))
    h = hasher.hexdigest()
    return h

@tryAction
def createAccount(connection, username, password, email):
    if(checkExists(connection, username) == True):
        return False
    cursor = connection.cursor(prepared=True)
    statement = "INSERT INTO User(username, email, hash, salt, standing) VALUES(%s, %s, %s, %s, %s)"
    maxint = 0xFFFFFFFFFFFFFFFF
    random.seed(int(time.time() * 1000))
    s = random.randint(0, maxint)
#    print("Generated Salt", s)
    h = hashSalt(password, s)
#    print("The hash is", h)
    cursor.execute(statement, (username, email, h, s, 1))
    connection.commit()
    cursor.close()
    return True
    
@tryAction
def checkPassword(connection, username, password):
    cursor = connection.cursor(prepared=True)
    select = "SELECT * FROM User WHERE username=%s AND hash=%s"
    getHash = "SELECT salt FROM User WHERE username=%s"
    cursor.execute(getHash, (username,))
    salt = 0
    fail = True
    for data in cursor:
        salt = data[0]
        fail = False
    if fail:
        return False
#        print("Grabbed salt: ", salt)
    h = hashSalt(password, salt)
#    print("The hash is", h)
    cursor.execute(select, (username, h))
    val = False
    for data in cursor:
        val = True
    cursor.close()
    return val
    
@tryAction
def checkExists(connection, username):
    cursor = connection.cursor(prepared=True)
    statement = "SELECT * FROM User WHERE username=%s"
    cursor.execute(statement, (username,))
    val = False
    for data in cursor:
        val = True
    cursor.close()
    return val
    
