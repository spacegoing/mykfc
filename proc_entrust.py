import kungfu
from kungfu.wingchun.constants import (
    InstrumentType,
    Side,
    ExecType,
    PriceType,
    Exchange,
)
from tqdm import tqdm

from pandas import read_csv
import re
from datetime import datetime
import pandas as pd


lf = kungfu.__binding__.longfist
wc = kungfu.__binding__.wingchun
yjj = kungfu.__binding__.yijinjing


import json

j = json.load(open("backtest_config.json", "r"))
symbol_exchange_map = {}
for data in j["Commission"]["default"]:
    symbol_exchange_map[data["product_id"]] = data["exchange_id"]

side_map = {"1": Side.Buy, "2": Side.Sell, "G": Side.Unknown, "F": Side.Unknown}
price_type_map = {"1": PriceType.Any, "2": PriceType.Limit, "U": PriceType.ForwardBest}


def get_exchange(instrumentID: str):
    product_id = "".join(re.findall("[A-Za-z]", instrumentID)).upper()
    return symbol_exchange_map[product_id]


def run(slice_tool: wc.SliceTool, csv_file, instrument_id):
    df = read_csv(csv_file)

    for row in tqdm(df.itertuples()):
        # 逐笔委托 entrust

        date_str = str(row.TransactTime)
        time_stamp = datetime.strptime(date_str, "%Y%m%d%H%M%S%f")
        dt = int(time_stamp.timestamp() * 1e9)

        entrust = lf.types.Entrust()

        entrust.data_time = dt
        entrust.instrument_id = instrument_id
        entrust.exchange_id = "SZE"
        entrust.instrument_type = InstrumentType.Stock
        entrust.main_seq = int(getattr(row, "ChannelNo"))
        entrust.seq = int(getattr(row, "ApplSeqNum"))
        entrust.price = float(getattr(row, "Price"))
        entrust.volume = float(getattr(row, "OrderQty"))

        side_ = getattr(row, "Side")
        if isinstance(side_, str):
            entrust.side = side_map[side_]
        else:
            entrust.side = side_map[str(int(side_))]

        price_t = getattr(row, "OrdType")
        # OrdType可能有空值,可能被转成浮点数,可能是字符串
        if pd.isna(price_t):
            entrust.price_type = PriceType.Limit
        else:
            price_t = price_t if isinstance(price_t, str) else str(int(price_t))
            entrust.price_type = price_type_map[price_t]

        # print(quote)
        slice_tool.write_at(dt, dt, 0, entrust)
