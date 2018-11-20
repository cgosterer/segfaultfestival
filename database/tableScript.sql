CREATE TABLE User (
	username	VARCHAR(50) PRIMARY KEY,
	email		VARCHAR(255),
	hash		BIGINT UNSIGNED,
	salt		BIGINT UNSIGNED,
	standing	BOOLEAN
);

CREATE TABLE Band (
	name		VARCHAR(50) PRIMARY KEY,
	websiteURL	VARCHAR(255),
	spotifyURL	VARCHAR(255),
	founded		DATE,
	active		BOOLEAN
);

CREATE TABLE Song (
	songName	VARCHAR(50),
	bandName	VARCHAR(50),
	album		VARCHAR(50),
	runTime		TIME,
	PRIMARY KEY (songName, bandName, album),
	FOREIGN KEY(bandName) REFERENCES Band(name)
);

CREATE TABLE Festival (
	name		VARCHAR(50),
	startDate	DATETIME,
	location	VARCHAR(50),
	websiteURL	VARCHAR(50),
	PRIMARY KEY (name, startDate)
);

CREATE TABLE FestivalSchedule (
	festivalName	VARCHAR(50),
	festivalStart	DATETIME,
	bandName	VARCHAR(50),
	performanceTime	DATETIME,
	FOREIGN KEY(festivalName, festivalStart) REFERENCES Festival(name, startDate),
	FOREIGN KEY(bandName) REFERENCES Band(name)
);

CREATE TABLE FavoritedSongs (
	user	VARCHAR(50) REFERENCES User(username),
	song	VARCHAR(50),
	band	VARCHAR(50),
	album	VARCHAR(50),
	FOREIGN KEY(song, band, album) REFERENCES Song(songName, bandName, album)
);

CREATE TABLE BandModeratorList (
	moderator	VARCHAR(50) NOT NULL,
	bandName	VARCHAR(50) NOT NULL,
	FOREIGN KEY(moderator) REFERENCES User(username),
	FOREIGN KEY(bandName) REFERENCES Band(name)
);

CREATE TABLE FestivalModeratorList (
	moderator	VARCHAR(50) NOT NULL,
	festivalName	VARCHAR(50) NOT NULL,
	FOREIGN KEY(moderator) REFERENCES User(username),
	FOREIGN KEY(festivalName) REFERENCES Festival(name)
);

CREATE TABLE AdminList (
	username	VARCHAR(50) REFERENCES User(username)
);
