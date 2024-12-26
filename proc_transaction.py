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

exec_type_map = {"4": ExecType.Cancel, "F": ExecType.Trade}


def get_exchange(instrumentID: str):
    product_id = "".join(re.findall("[A-Za-z]", instrumentID)).upper()
    return symbol_exchange_map[product_id]

def run(slice_tool: wc.SliceTool, csv_file, instrument_id):
    df = read_csv(csv_file)

    for row in tqdm(df.itertuples()):
        # 逐笔成交 transaction

        date_str = str(row.TransactTime)
        time_stamp = datetime.strptime(date_str, "%Y%m%d%H%M%S%f")
        dt = int(time_stamp.timestamp() * 1e9)

        transaction = lf.types.Transaction()

        transaction.data_time = dt
        transaction.instrument_id = instrument_id
        transaction.exchange_id = "SZE"
        transaction.instrument_type = InstrumentType.Stock
        transaction.main_seq = int(getattr(row, "ChannelNo"))
        transaction.seq = int(getattr(row, "ApplSeqNum"))
        transaction.bid_no = int(getattr(row, "BidApplSeqNum"))
        transaction.ask_no = int(getattr(row, "OfferApplSeqNum"))
        transaction.price = float(getattr(row, "Price"))
        transaction.volume = float(getattr(row, "Qty"))

        transaction.exec_type = exec_type_map[getattr(row, "ExecType")]

        # transaction.side由买卖订单号大小决定
        if transaction.bid_no > transaction.ask_no:
            transaction.side = Side.Buy
        elif transaction.bid_no < transaction.ask_no:
            transaction.side = Side.Sell
        else:
            transaction.side = Side.Unknown

        # print(quote)
        slice_tool.write_at(dt, dt, 0, transaction)
