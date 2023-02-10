/* TGT Table - weather_data */

CREATE TABLE IF NOT EXISTS weather_data (
	rid INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    weather_station TEXT NOT NULL,
    record_date INTEGER NOT NULL,
	max_temp INTEGER NOT NULL,
	min_temp INTEGER NOT NULL,
	precipitation INTEGER NOT NULL,
    UNIQUE(weather_station, record_date)
);
