"""
Script for storing into DB rate IN and rate Out
"""

from my_utils import get_ipfs_stats_bw, create_table, put_into_db
import sqlite3
import time


DB_fname     = "ipfs_traffic.db"
REFRESH_RATE = 1 # Seconds
SAVE_RATE    = 60
VERBOSE      = True


if __name__ == "__main__":
    try:
        conn = sqlite3.connect(DB_fname)
        c    = conn.cursor()
        create_table(c)

        cnt = 0

        while True:

            dic_stats = get_ipfs_stats_bw()
            if VERBOSE:
                print(dic_stats)

            put_into_db(c, dic_stats)

            cnt += 1
            if cnt % SAVE_RATE == 0:
                conn.commit()

            time.sleep(REFRESH_RATE)

    except KeyboardInterrupt:
        conn.commit()
        conn.close()
        pass
else:
    print(__name__)
    print("Closing")