/* TGT Table - weather_stats */

CREATE TABLE IF NOT EXISTS weather_stats (
	rid INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    record_year INTEGER NOT NULL,
    weather_station TEXT NOT NULL,
	avg_max_temp DECIMAL(5,2) NOT NULL,
	avg_min_temp DECIMAL(5,2) NOT NULL,
	tot_precipitation DECIMAL(5,2) NOT NULL,
    UNIQUE(weather_station, record_year)
);
