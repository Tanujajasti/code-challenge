/* TGT Table - weather_stats */

CREATE TABLE IF NOT EXISTS weather_stats (
	data_key INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    record_year INTEGER NOT NULL,
    weather_station TEXT NOT NULL,
	avg_max_temp INTEGER NOT NULL,
	avg_min_temp INTEGER NOT NULL,
	tot_precipitation INTEGER NOT NULL,
    UNIQUE(weather_station, record_year)
);
