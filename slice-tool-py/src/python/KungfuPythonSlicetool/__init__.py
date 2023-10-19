import kungfu
from kungfu.wingchun.constants import InstrumentType
from tqdm import tqdm

from pandas import read_csv
import re

lf = kungfu.__binding__.longfist
wc = kungfu.__binding__.wingchun
yjj = kungfu.__binding__.yijinjing


import json
j = json.load(open("backtest_config.json", "r"))
symbol_exchange_map = {}
for data in j["Commission"]["default"]:
    symbol_exchange_map[data["product_id"]] = data["exchange_id"]

def get_exchange(instrumentID: str):
    product_id = ''.join(re.findall('[A-Za-z]', instrumentID)).upper()
    return symbol_exchange_map[product_id]

def run(slice_tool: wc.SliceTool):    
    df = read_csv(slice_tool.arguments)
    for row in tqdm(df.itertuples()):
        dt = row.rvTime

        quote = lf.types.Quote()
        
        quote.data_time = dt
        
        quote.instrument_id = getattr(row, "instrumentID")
        quote.exchange_id = get_exchange(quote.instrument_id)
        
        quote.instrument_type = InstrumentType.Future
                
        quote.last_price = getattr(row, "lastPrice")
        quote.volume = getattr(row, "volume")
        
        quote.open_interest = getattr(row, "openInterest")
        
        quote.bid_price = [getattr(row, "bid")]
        quote.bid_volume = [getattr(row, "bidVolume")]
        quote.ask_price = [getattr(row, "ask")]
        quote.ask_volume = [getattr(row, "askVolume")]

        # print(quote)
        slice_tool.write_at(dt, dt, 0, quote)


