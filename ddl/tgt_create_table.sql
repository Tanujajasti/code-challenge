/* TGT Table - weather_data */

CREATE TABLE IF NOT EXISTS weather_data (
	rid INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    weather_station TEXT NOT NULL,
    record_date INTEGER NOT NULL,
	max_temp DECIMAL(5,2) NOT NULL,
	min_temp DECIMAL(5,2) NOT NULL,
	precipitation DECIMAL(5,2) NOT NULL,
    UNIQUE(weather_station, record_date)
);
