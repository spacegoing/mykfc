import glob
import pandas as pd
import numpy as np
import datetime
import fnmatch
import gzip
from pathlib import Path
from ctypes import c_double, c_int64

# Create a list of all relevant .gz files 
with open("品种映射表.csv") as f:
	csv_data = f.read()
name_map = {}

for line in csv_data.splitlines()[1:]:
	fields = line.split(',')
	name_map[fields[0].split('_')[0]] = fields[1]
print(name_map)

files = glob.glob('snapshot/*.gz')
# Iterate through the list and parse each file
dataframes = []
for path_to_file in files:
    if fnmatch.fnmatch(Path(path_to_file).name, 'BBHBeat*'):
        continue
    instrument_id = name_map[Path(path_to_file).name.split('_')[0]] + Path(path_to_file).name.split('_')[1]
    dtype = [("ask", c_double),
            ("bid", c_double),
            ("lastPrice", c_double),
            ("vwapPrice", c_double),
            ("askVolume", c_int64),
            ("bidVolume", c_int64),
            ("volume",    c_int64),
            ("openInterest", c_int64),
            ("dsTime", c_int64),
            ("rvTime", c_int64)]
    with gzip.GzipFile(path_to_file, "rb") as f:
            a = np.frombuffer(f.read(), dtype=dtype)
    df = pd.DataFrame(a)
    df['dsTime'] = df['dsTime'] * 1000000
    df['rvTime'] = df['rvTime'] * 1000000
    df = df.reindex(['dsTime', 'rvTime', 'ask', 'bid',
                       'lastPrice', 'vwapPrice', 'askVolume',
                      'bidVolume', 'volume', 'openInterest'], axis = 1)
    df['instrumentID'] = instrument_id
    # Append the parsed DataFrame to a list for future use
    dataframes.append(df)

# Combine all the dataframes and sort by rvTime
combined_df = pd.concat(dataframes).sort_values(by="rvTime")
combined_df = combined_df.reset_index(drop=True)
combined_df.to_csv('snapshot.csv', )