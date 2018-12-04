import mysql.connector

def addSong(connection, bandName, songName, album):
    cursor = connection.cursor(prepared=True)
    statement = "INSERT INTO Song(songName, bandName, album) VALUES(%s, %s, %s);"
    cursor.execute(statement, (songName, bandName, album))
    cursor.close()
    connection.commit()

def removeSong(connection, bandName, songName, album):
    cursor = connection.cursor(prepared=True)
    statement = "DELETE FROM Song WHERE songName=%s AND bandName=%s AND album=%s;"
    cursor.execute(statement, (songName, bandName, album))
    cursor.close()
    connection.commit()

def updateFoundingDate(connection, band, date):
    cursor = connection.cursor(prepared=True)
    statement = "UPDATE Band SET founded=%s WHERE bandName=%s;"
    cursor.execute(statement, (date, band))
    cursor.close()
    connection.commit()

def setActive(connection, band):
    cursor = connection.cursor(prepared=True)
    statement = "UPDATE Band SET active=True WHERE bandName=%s;"
    cursor.execute(statement, (band,))
    cursor.close()
    connection.commit()

def setInactive(connection, band):
    cursor = connection.cursor(prepared=True)
    statement = "UPDATE Band SET active=False WHERE bandName=%s;"
    cursor.execute(statement, (band,))
    cursor.close()
    connection.commit()

def addMod(connection, band, user):
    cursor = connection.cursor(prepared=True)
    statement = "INSERT INTO BandModeratorList(moderator, bandName) VALUES(%s, %s);"
    cursor.execute(statement, (user, band))
    cursor.close()
    connection.commit()

def removeMod(connection, band, user):
    cursor = connection.cursor(prepared=True)
    statement = "DELETE FROM BandModeratorList WHERE bandName=%s AND moderator=%s"
    cursor.execute(statement, (band, user))
    cursor.close()
    connection.commit()

def setSpotify(connection, band, url):
    cursor = connection.cursor(prepared=True)
    statement = "UPDATE Band SET spotifyURL=%s WHERE bandName=%s;"
    cursor.execute(statement, (url, band))
    connection.commit()
    cursor.close()

def setWebsite(connection, band, url):
    cursor = connection.cursor(prepared=True)
    statement = "UPDATE Band SET websiteURL=%s WHERE bandName=%s;"
    cursor.execute(statement, (url, band))
    connection.commit()
    cursor.close()
