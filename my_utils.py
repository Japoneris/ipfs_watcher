import time
import subprocess
import sqlite3


#################
# IPFS #
#################
bashCommand = "ipfs stats bw"

def unit_decode(unit, default=1):
    """Transform 
    - b* -> 1
    - kb* -> 1000
    - mb* -> 10**6
    - gb* -> 10**9
    """
    
    ul    = unit.lower()
    units = [("kb", 1000), ("mb", 10**6), ("gb", 10**9), ("tb", 10**12)]
    for (u, v) in units:
        if u in ul:
            return v
    
    return default


def get_ipfs_stats_bw():
    process       = subprocess.Popen(bashCommand.split(), stdout=subprocess.PIPE)
    output, error = process.communicate()

    if len(output) == 0:
        return
    
    
    try:
        params = output.decode().replace(":", "").split()[1:]
        return dict([(params[i*3], float(params[1+i*3]) * unit_decode(params[2 + i*3])) 
                     for i in range(4)])
    except:
        return {}
    
#########################
# DB #
#########################

def db_helper():
    print("How to make it work")
    print("""
    conn = sqlite3.connect("<whatever_db>.db")
    c = conn.cursor()
    
    create_table(c)
    conn.commit()
    
    while True:
        
        time.sleep(1)
        dic_stats = get_ipfs_stats_bw()
        put_into_db(dic_stats, c)
        print(dic_stats)
    
    """)
    

def create_table(c, name="traffic"):

    c.execute("""CREATE TABLE IF NOT EXISTS {} (
      time        TIMESTAMPTZ       NOT NULL,
      RateIn      REAL              NOT NULL,
      RateOut     REAL              NOT NULL
    );
    """.format(name))
    return True


def put_into_db(c, dic, name="traffic"):
    """
    t0: time of DBquery (must be approximately time of IPFS Query)
    """
    t0 = int(time.time())
    v_in  = dic["RateIn"]
    v_out = dic["RateOut"]

    c.execute("""INSERT INTO {} (time, RateIn, RateOut)
                 VALUES ({}, {}, {})
    """.format(name, t0, v_in, v_out))

    return True