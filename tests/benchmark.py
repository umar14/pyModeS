import sys
import time
import pandas as pd
from tqdm import tqdm

fin = sys.argv[1]

df = pd.read_csv(fin, names=["ts", "df", "icao", "msg"])
df_adsb = df[df["df"] == 17].copy()

total = df_adsb.shape[0]


def native():

    from pyModeS.decoder import adsb
    from pyModeS.decoder import common

    msg0 = None
    msg1 = None

    for i, r in tqdm(df_adsb.iterrows(), total=total):
        ts = r.ts
        m = r.msg.encode()

        downlink_format = common.df(m)
        crc = common.crc(m)
        icao = adsb.icao(m)
        tc = adsb.typecode(m)

        if 1 <= tc <= 4:
            category = adsb.category(m)
            callsign = adsb.callsign(m)
        if tc == 19:
            velocity = adsb.velocity(m)
        if 5 <= tc <= 18:
            if adsb.oe_flag(m):
                msg1 = m
                t1 = ts
            else:
                msg0 = m
                t0 = ts

            if msg0 and msg1:
                try:
                    position = adsb.position(msg0, msg1, t0, t1)
                except:
                    continue
                altitude = adsb.altitude(m)


def cython():

    from pyModeS.c_decoder import adsb
    from pyModeS.c_decoder import common

    msg0 = None
    msg1 = None

    for i, r in tqdm(df_adsb.iterrows(), total=total):
        ts = r.ts
        m = r.msg.encode()

        downlink_format = common.df(m)
        crc = common.crc(m)
        icao = adsb.icao(m)
        tc = adsb.typecode(m)

        if 1 <= tc <= 4:
            category = adsb.category(m)
            callsign = adsb.callsign(m)
        if tc == 19:
            velocity = adsb.velocity(m)
        if 5 <= tc <= 18:
            if adsb.oe_flag(m):
                msg1 = m
                t1 = ts
            else:
                msg0 = m
                t0 = ts

            if msg0 and msg1:
                try:
                    position = adsb.position(msg0, msg1, t0, t1)
                except:
                    continue
                altitude = adsb.altitude(m)


if __name__ == "__main__":
    t1 = time.time()
    native()
    dt1 = time.time() - t1

    t2 = time.time()
    cython()
    dt2 = time.time() - t2