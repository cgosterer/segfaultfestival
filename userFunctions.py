import mysql.connector

def getLikeCount(connection, band):
    cursor = connection.cursor(prepared=True)
    statement = "SELECT * FROM bandLikes WHERE bandName=%s;"
    cursor.execute(statement, (band,))
    num = 0;
    for data in cursor:
        num += 1
    cursor.close()
    return num

def like(connection, band, user):
    cursor = connection.cursor(prepared=True)
    statement = "INSERT INTO bandLikes(bandName, username) VALUES(%s, %s);"
    cursor.execute(statement, (band, user))
    cursor.close()
    
def createPage(connection, user, band):
    cursor = connection.cursor(prepared=True)
    statement = "SELECT * FROM Bands WHERE name=%s;"
    cursor.execute(statement, (band,))
    for data in cursor:
        return False
    statement = "INSERT INTO Bands(name) VALUES(band);"
    cursor.execute(statement, (band,))
    statement = "INSERT INTO BandModeratorList(bandName, moderator) VALUES(%s, %s);"
    cursor.execute(statement, (band, user))
    connection.commit()
    cursor.close()
    
