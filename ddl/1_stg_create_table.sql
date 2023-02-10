/* stage Weather Table */

CREATE TABLE IF NOT EXISTS stg_weather_data (
    record_date INTEGER NOT NULL,
	max_temp INTEGER NOT NULL,
	min_temp INTEGER NOT NULL,
	precipitation INTEGER NOT NULL
);
