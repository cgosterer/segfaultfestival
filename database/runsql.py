import mysql.connector
from mysql.connector import errorcode
import sys

def runScript(cn, filename):
    cursor = cn.cursor()
    f = open(filename, 'r')
    text = f.read()
    try:
        print("Running command:")
        print(text)
        cursor.execute(text)
        for data in cursor:
            print(data)
    except mysql.connector.Error as err:
        print(err.msg)
    else:
        print("Successful!")
    cn.commit()
    cursor.close()

if __name__ == '__main__':
    if len(sys.argv) != 2:
        print("Incorrect number of arguments")
        exit()
    try:
        cnx = mysql.connector.connect(user='dbtest4020',
                               password='Pp0gHfo-~149',
                               host='den1.mysql1.gear.host',
                               database='dbtest4020')
    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            print("Something is wrong with your user name or password")
        elif err.errno == errorcode.ER_BAD_DB_ERROR:
            print("Database does not exist")
        else:
            print(err)
    else:
        print("Connection established")
        runScript(cnx, sys.argv[1])
        cnx.close()
