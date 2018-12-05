import mysql.connector
from tryAction import tryAction

@tryAction
def addSong(connection, bandName, songName, album):
    cursor = connection.cursor(prepared=True)
    statement = "INSERT INTO Song(songName, bandName, album) VALUES(%s, %s, %s);"
    check = "SELECT * FROM Band WHERE name=%s;"
    cursor.execute(check, (bandName,))
    for data in cursor:
        cursor.execute(statement, (songName, bandName, album))
        cursor.close()
        connection.commit()
        return True
    cursor.close()
    return False

@tryAction
def removeSong(connection, bandName, songName, album):
    cursor = connection.cursor(prepared=True)
    statement = "DELETE FROM Song WHERE songName=%s AND bandName=%s AND album=%s;"
    cursor.execute(statement, (songName, bandName, album))
    cursor.close()
    connection.commit()
    return True

@tryAction
def updateFoundingDate(connection, band, date):
    cursor = connection.cursor(prepared=True)
    statement = "UPDATE Band SET founded=%s WHERE bandName=%s;"
    check = "SELECT * FROM Band WHERE bandName=%s;"
    cursor.execute(check, (band,))
    for data in cursor:
        cursor.execute(statement, (date, band))
        cursor.close()
        connection.commit()
        return True
    cursor.close()
    return False

@tryAction
def setActive(connection, band):
    cursor = connection.cursor(prepared=True)
    statement = "UPDATE Band SET active=True WHERE bandName=%s;"
    check = "SELECT * FROM Band WHERE bandName=%s;"
    cursor.execute(check, (band,))
    for data in cursor:
        cursor.execute(statement, (band,))
        cursor.close()
        connection.commit()
        return True
    cursor.close()
    return False

@tryAction
def setInactive(connection, band):
    cursor = connection.cursor(prepared=True)
    statement = "UPDATE Band SET active=False WHERE bandName=%s;"
    check = "SELECT * FROM Band WHERE bandName=%s;"
    cursor.execute(check, (band,))
    for data in cursor:
        cursor.execute(statement, (band,))
        cursor.close()
        connection.commit()
        return True
    cursor.close()
    return False

@tryAction
def addMod(connection, band, user):
    cursor = connection.cursor(prepared=True)
    statement = "INSERT INTO BandModeratorList(moderator, bandName) VALUES(%s, %s);"
    check = "SELECT * FROM Band WHERE bandName=%s;"
    cursor.execute(check, (band,))
    for data in cursor:
        cursor.execute(statement, (user, band))
        cursor.close()
        connection.commit()
        return True
    cursor.close()
    return False

@tryAction
def removeMod(connection, band, user):
    cursor = connection.cursor(prepared=True)
    statement = "DELETE FROM BandModeratorList WHERE bandName=%s AND moderator=%s"
    check = "SELECT * FROM Band WHERE bandName=%s;"
    cursor.execute(check, (band,))
    for data in cursor:
        cursor.execute(statement, (band, user))
        cursor.close()
        connection.commit()
        return True
    cursor.close()
    return False

@tryAction
def setSpotify(connection, band, url):
    cursor = connection.cursor(prepared=True)
    statement = "UPDATE Band SET spotifyURL=%s WHERE bandName=%s;"
    check = "SELECT * FROM Band WHERE bandName=%s;"
    cursor.execute(check, (band,))
    for data in cursor:
        cursor.execute(statement, (url, band))
        connection.commit()
        cursor.close()
        return True
    cursor.close()
    return False

@tryAction
def setWebsite(connection, band, url):
    cursor = connection.cursor(prepared=True)
    statement = "UPDATE Band SET websiteURL=%s WHERE bandName=%s;"
    check = "SELECT * FROM Band WHERE bandName=%s;"
    cursor.execute(check, (band,))
    for data in cursor:
        cursor.execute(statement, (url, band))
        connection.commit()
        cursor.close()
        return True
    cursor.close()
    return False
