import os, sqlite3
import unicodecsv
from datetime import datetime

STG_TABLE = "stg_weather_data"
TGT_TABLE = "weather_data"
STATS_TABLE = "weather_stats"

con = sqlite3.connect("main.db")
cur = con.cursor()


def get_file_content(file_name):
    with open(file_name) as f:
        data = f.read()
    return data


def exec_query_from_file(file_name):
    query = get_file_content(file_name)
    cur.execute(query)


def read_file(file_name, delim="\t"):
    with open(file_name, "rb") as input_file:
        reader = unicodecsv.reader(input_file, delimiter=delim)
        data = [row for row in reader]
    return data


def get_table_count(table_name):
    result = cur.execute(f"SELECT count(1) from {table_name};")
    return result.fetchone()[0]


def main(files):
    for file in files:
        data = read_file(f"wx_data/{file}")
        cur.execute(f"DELETE FROM {STG_TABLE};")
        cur.executemany(
            f"INSERT INTO {STG_TABLE} VALUES (?, ?, ?, ?);",
            data,
        )

        print(f"File name: {file}")
        print(f"Stg table loaded: {get_table_count(STG_TABLE)}")

        weather_station = file.split(".")[0]
        records_to_insert = cur.execute(
            f"""SELECT count(1) 
            from {STG_TABLE} st 
            where record_date not in (select record_date from {TGT_TABLE} where weather_station = '{weather_station}');
            """
        ).fetchone()[0]

        print(f"Total records to insert: {records_to_insert}")

        if records_to_insert:
            cur.execute(
                f"""INSERT or IGNORE INTO {TGT_TABLE} 
                SELECT null, '{weather_station}', record_date, max_temp/10 as max_temp, min_temp/10 as min_temp, precipitation/100 as precipitation
                FROM {STG_TABLE}"""
            )

        print(f"Current target table record count: {get_table_count(TGT_TABLE)}")
        print()


def main_stats():
    window_func_query = "SELECT distinct weather_station, substr(record_date, 1, 4) as record_year, {func}({col_nm}) over(partition by weather_station, substr(record_date, 1, 4)) as {col_nm} FROM {TGT_TABLE} WHERE {col_nm} != -9999"

    cur.execute(
        f"""
        INSERT or IGNORE INTO {STATS_TABLE}
        select null, mx_t.record_year, mx_t.weather_station, mx_t.max_temp, mn_t.min_temp, tot_pr.precipitation
        from ({window_func_query.format(func="avg", col_nm="max_temp", TGT_TABLE=TGT_TABLE)}) mx_t
        join ({window_func_query.format(func="avg", col_nm="min_temp", TGT_TABLE=TGT_TABLE)}) mn_t
        on mx_t.weather_station = mn_t.weather_station and mx_t.record_year = mn_t.record_year
        join ({window_func_query.format(func="sum", col_nm="precipitation", TGT_TABLE=TGT_TABLE)}) tot_pr
        on mn_t.weather_station = tot_pr.weather_station and mn_t.record_year = tot_pr.record_year
        """
    )
    print(f"Record count of stats table: {get_table_count(STATS_TABLE)}")


if __name__ == "__main__":
    exec_query_from_file("./ddl/stg_create_table.sql")
    exec_query_from_file("./ddl/tgt_create_table.sql")
    exec_query_from_file("./ddl/create_stats_table.sql")

    files = os.listdir(os.path.join(os.getcwd(), "wx_data"))

    # Inserting data into Stg and Target tables
    start_time = datetime.now()
    main(files)
    end_time = datetime.now()
    print("Total Duration (Source data ingestion): {}".format(end_time - start_time))
    print()

    # Inserting the stats table data
    print("Started Inserting the stats table data...")
    start_time = datetime.now()
    main_stats()
    end_time = datetime.now()
    print("Total Duration (Stats Data ingestion): {}".format(end_time - start_time))

    con.commit()
