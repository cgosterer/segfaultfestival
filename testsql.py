import mysql.connector
from mysql.connector import errorcode

def createTable(cn):
    cursor = cn.cursor()
    try:
        print("Creating Table Test_Table ", end='')
        cursor.execute("CREATE TABLE Test_Table (data int);")
    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_TABLE_EXISTS_ERROR:
            print("already exists.")
        else:
            print(err.msg)
    else:
        print("creation successful!")

    cursor.close()

def getTable(cn):
    cursor = cn.cursor()
    cursor.execute("SHOW TABLES;")
    for table in cursor:
        print(table)
    cursor.close()
    
if __name__ == '__main__':
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
        print("It worked")
        getTable(cnx)
        cnx.close()
