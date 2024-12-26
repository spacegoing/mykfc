import kungfu
from kungfu.wingchun.constants import InstrumentType
from tqdm import tqdm

from pandas import read_csv
import re
from datetime import datetime

lf = kungfu.__binding__.longfist
wc = kungfu.__binding__.wingchun
yjj = kungfu.__binding__.yijinjing


import json

j = json.load(open("backtest_config.json", "r"))
symbol_exchange_map = {}
for data in j["Commission"]["default"]:
    symbol_exchange_map[data["product_id"]] = data["exchange_id"]


def get_exchange(instrumentID: str):
    product_id = "".join(re.findall("[A-Za-z]", instrumentID)).upper()
    return symbol_exchange_map[product_id]


def run(slice_tool: wc.SliceTool, csv_file, instrument_id):
    df = read_csv(csv_file)

    for row in tqdm(df.itertuples()):
        # l1 快照
        date_str = str(row.QuotTime)
        time_stamp = datetime.strptime(date_str, "%Y%m%d%H%M%S%f")
        dt = int(time_stamp.timestamp() * 1e9)

        quote = lf.types.Quote()

        quote.data_time = dt
        quote.instrument_id = instrument_id
        quote.exchange_id = "SZE"
        quote.instrument_type = InstrumentType.Stock
        quote.pre_close_price = float(getattr(row, "PreClosePx"))
        quote.last_price = float(getattr(row, "LastPx"))
        quote.volume = float(getattr(row, "Volume"))
        quote.turnover = float(getattr(row, "Amount"))
        quote.open_price = float(getattr(row, "OpenPx"))
        quote.high_price = float(getattr(row, "HighPx"))
        quote.low_price = float(getattr(row, "LowPx"))
        quote.close_price = int(getattr(row, "ClosePx"))
        quote.bid_price = eval(getattr(row, "BidPrice"))
        quote.bid_volume = eval(getattr(row, "BidOrderQty"))
        quote.ask_price = eval(getattr(row, "OfferPrice"))
        quote.ask_volume = eval(getattr(row, "OfferQty"))
        quote.total_trade_num = int(getattr(row, "NumTrades"))
        quote.trading_phase_code = str(getattr(row, "TradingPhaseCode"))

        # print(quote)
        slice_tool.write_at(dt, dt, 0, quote)
