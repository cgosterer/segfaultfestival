import mysql.connector
from tryAction import tryAction

@tryAction
def getLikeCount(connection, band):
    cursor = connection.cursor(prepared=True)
    statement = "SELECT * FROM bandLikes WHERE bandName=%s;"
    cursor.execute(statement, (band,))
    num = 0;
    for data in cursor:
        num += 1
    cursor.close()
    return num

@tryAction
def like(connection, band, user):
    cursor = connection.cursor(prepared=True)
    statement = "INSERT INTO bandLikes(bandName, username) VALUES(%s, %s);"
    check = "SELECT * FROM Band WHERE name=%s;"
    cursor.execute(check, (band,))
    for data in cursor:
        cursor.execute(statement, (band, user))
        connection.commit()
        cursor.close()
        return True
    cursor.close()
    return False

@tryAction
def likeSong(connection, user, song, band, album):
    cursor = connection.cursor(prepared=True)
    statement = "INSERT INTO FavoritedSongs(user, song, band, album) VALUES(%s, %s, %s, %s);"
    check = "SELECT * FROM Song WHERE songName=%s AND bandName=%s AND album=%s;"
    cursor.execute(check, (song, band, album))
    for data in cursor:
        cursor.execute(statement, (user, song, band, album))
        connection.commit()
        cursor.close()
        return True
    cursor.close()
    return False

@tryAction
def unlinkeBand(connection, user, band):
    cursor = connection.cursor(prepared=True)
    statement = "DELETE FROM bandLikes WHERE bandname=%s AND username=%s;"
    check = "SELECT * FROM bandLikes WHERE bandname=%s AND username=%s;"
    cursor.execute(check, (band, user))
    for data in cursor:
        cursor.execute(statement, (band, user))
        connection.commit()
        cursor.close()
        return True
    cursor.close()
    return False

@tryAction
def unlikeSong(connection, user, song, band, album):
    cursor = connection.cursor(prepared=True)
    statement = "DELETE FROM FavoritedSongs WHERE user=%s AND song=%s AND band=%s AND album=%s;"
    check = "SELECT * FROM FavoritedSongs WHERE user=%s AND song=%s AND band=%s AND album=%s;"
    cursor.execute(check, (user, song, band, album))
    for data in cursor:
        cursor.execute(statement, (user, song, band, album))
        connection.commit()
        cursor.close()
        return True
    cursor.close()
    return False

@tryAction
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
    return True
