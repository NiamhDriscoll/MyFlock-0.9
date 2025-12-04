CREATE TABLE flocks(
	id INTEGER PRIMARY KEY,
	
	user_id INTEGER NOT NULL REFERENCES users(id)
);

CREATE TABLE flock_members(
	
	role TEXT NOT NULL,
	user_id INTEGER NOT NULL REFERENCES users(id),
	flock_id INTEGER NOT NULL REFERENCES flocks(id)
);


CREATE TABLE birds(
	id INTEGER PRIMARY KEY,
	breed TEXT NOT NULL,
	birth_date DATE NOT NULL,
	name TEXT NOT NULL,
	info TEXT,
	flock_id INTEGER NOT NULL REFERENCES flocks(id)
);

CREATE TABLE users(
	username TEXT,
	email TEXT,
	password TEXT,
	id INTEGER PRIMARY KEY
);
