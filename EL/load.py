import psycopg2
from psycopg2 import extras

from config import DB_CONFIG

def saving(races, drivers, results):
    conn: psycopg2.extensions.connection = psycopg2.connect(**DB_CONFIG, cursor_factory=extras.RealDictCursor)
    cur: psycopg2.extensions.cursor = conn.cursor()

    # 1. Create staging tables (if they don't exist yet)
    cur.execute('''
        CREATE TABLE IF NOT EXISTS raw_races (
            year                      INTEGER,
            grand_prix                VARCHAR(100),
            url                       VARCHAR(255),
            date                      VARCHAR(20),
            winner_driver_first_name  VARCHAR(50),
            winner_driver_last_name   VARCHAR(50),
            winner_driver_short_name  CHAR(3),
            winner_team               VARCHAR(100),
            winner_laps               VARCHAR(10),
            winner_time               VARCHAR(20)
        );

        CREATE TABLE IF NOT EXISTS raw_drivers (
            year                      INTEGER,
            driver_first_name         VARCHAR(50),
            driver_last_name          VARCHAR(50),
            driver_short_name         CHAR(3),
            driver_url                VARCHAR(255),
            driver_nationality        CHAR(3),
            team                      VARCHAR(100),
            team_url                  VARCHAR(255),
            pts                       VARCHAR(10)
        );

        CREATE TABLE IF NOT EXISTS raw_results (
            url                       VARCHAR(255),
            pos                       VARCHAR(10),
            no                        VARCHAR(10),
            driver_first_name         VARCHAR(50),
            driver_last_name          VARCHAR(50),
            driver_short_name         CHAR(3),
            team                      VARCHAR(100),
            laps                      VARCHAR(10),
            time_retired              VARCHAR(30),
            pts                       VARCHAR(10)
        );
    ''')

    # 2. Insert the data as it is
    print('saving...')

    for r in races:
        cur.execute('''
            INSERT INTO raw_races VALUES (
                %(year)s, 
                %(grand_prix)s, 
                %(url)s, 
                %(date)s, 
                %(winner_driver_first_name)s, 
                %(winner_driver_last_name)s, 
                %(winner_driver_short_name)s, 
                %(winner_team)s, 
                %(winner_laps)s, 
                %(winner_time)s
            )
        ''', {
            'year':                     r['year'], 
            'grand_prix':               r['grand_prix'], 
            'url':                      r['url'], 
            'date':                     r['date'],
            'winner_driver_first_name': r['winner_driver_first_name'], 
            'winner_driver_last_name':  r['winner_driver_last_name'],
            'winner_driver_short_name': r['winner_driver_short_name'], 
            'winner_team':              r['winner_team'],
            'winner_laps':              r['winner_laps'], 
            'winner_time':              r['winner_time']
        })

    for d in drivers:
        cur.execute('''
            INSERT INTO raw_drivers VALUES (
                %(year)s, 
                %(first_name)s, 
                %(last_name)s, 
                %(short_name)s, 
                %(url)s, 
                %(nationality)s, 
                %(team)s, 
                %(team_url)s, 
                %(pts)s
            )
        ''', {
            'year':               d['year'], 
            'first_name':         d['first_name'], 
            'last_name':          d['last_name'],
            'short_name':         d['short_name'], 
            'url':                d['url'], 
            'nationality':        d['nationality'],
            'team':               d['team'], 
            'team_url':           d['team_url'], 
            'pts':                d['pts']
        })

    for res in results:
        cur.execute('''
            INSERT INTO raw_results VALUES (
                %(url)s, 
                %(po)s, 
                %(no)s, 
                %(driver_first_name)s, 
                %(driver_last_name)s, 
                %(driver_short_name)s, 
                %(team)s, 
                %(laps)s, 
                %(time)s, 
                %(pts)s
            )
        ''', {
            'url':               res['url'], 
            'po':                res['po'], 
            'no':                res['no'], 
            'driver_first_name': res['driver_first_name'],
            'driver_last_name':  res['driver_last_name'], 
            'driver_short_name': res['driver_short_name'], 
            'team':              res['team'],
            'laps':              res['laps'], 
            'time':              res['time'], 
            'pts':               res['pts']
        })

    conn.commit()
    cur.close()
    conn.close()
    print('saved to f1_db')


if __name__ == '__main__':
    import pandas as pd
    races = pd.read_csv('./sample/races.csv').to_dict(orient='records')
    drivers = pd.read_csv('./sample/drivers.csv').to_dict(orient='records')
    results = pd.read_csv('./sample/results.csv').to_dict(orient='records')
    saving(races, drivers, results)