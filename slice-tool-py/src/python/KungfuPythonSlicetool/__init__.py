import os
import kungfu
from kungfu.wingchun.constants import InstrumentType
from tqdm import tqdm

from pandas import read_csv
import re

lf = kungfu.__binding__.longfist
wc = kungfu.__binding__.wingchun
yjj = kungfu.__binding__.yijinjing


import json
from .proc_entrust import run as enrun
from .proc_quote import run as qrun
from .proc_transaction import run as trun

j = json.load(open("backtest_config.json", "r"))
symbol_exchange_map = {}
for data in j["Commission"]["default"]:
    symbol_exchange_map[data["product_id"]] = data["exchange_id"]


def get_exchange(instrumentID: str):
    product_id = "".join(re.findall("[A-Za-z]", instrumentID)).upper()
    return symbol_exchange_map[product_id]


# %% Configuration
stock_list = ["000001"]
data_dir = "/workspace/host_folder/kftest/kfdata/"


# Function to directly check for specific files
def find_files_directly(base_dir, stock_list):
    matching_files = []

    for root, dirs, _ in os.walk(base_dir):
        for folder in dirs:
            for stock in stock_list:
                file_path = os.path.join(root, folder, f"{stock}.csv")
                if os.path.isfile(file_path):
                    matching_files.append(os.path.abspath(file_path))

    return matching_files


# Find files
result_files = find_files_directly(data_dir, stock_list)


def run(slice_tool: wc.SliceTool):
    for path in result_files:
        instrument_id = os.path.basename(path)
        if 'L1' in path:
            qrun(slice_tool, path, instrument_id)
        if 'tick' in path:
            trun(slice_tool, path, instrument_id)
        if 'order' in path:
            enrun(slice_tool, path, instrument_id)

