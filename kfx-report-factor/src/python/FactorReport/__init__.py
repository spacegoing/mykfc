from collections import defaultdict
from copy import copy
import kungfu
from pandas import DataFrame, Series
from scipy.stats import pearsonr, spearmanr, ttest_1samp

import json
from typing import Text
from kungfu.yijinjing import time as kft
from kungfu.wingchun.constants import *



lf = kungfu.__binding__.longfist
wc = kungfu.__binding__.wingchun
yjj = kungfu.__binding__.yijinjing

def calculate_cross_section_ic(x_df: DataFrame, y_df: DataFrame, rank: bool = False):
    """计算横截面IC"""
    if rank:
        # 截面因子排序IC
        func = spearmanr
    else:
        # 截面因子数值IC
        func = pearsonr
    x_df.dropna(inplace=True)
    y_df.dropna(inplace=True)
    # 整合索引
    new_index = x_df.index.join(y_df.index, how="inner")
    x_df = x_df.reindex(new_index)
    y_df = y_df.reindex(new_index)

    # 计算IC数值
    ic_data = []
    for x_row, y_row in zip(x_df.iterrows(), y_df.iterrows()):
        ic, _ = func(x_row[1], y_row[1])
        ic_data.append(ic)
    return Series(ic_data, index=new_index)


def calculate_time_series_ic(
    x_df: DataFrame,
    y_df: DataFrame,
    period = 0
):
    """计算时序IC"""
    x_df.dropna(inplace=True)
    y_df.dropna(inplace=True)
    # 整合索引
    new_index = x_df.index.join(y_df.index, how="inner")
    x_df = x_df.reindex(new_index)
    y_df = y_df.reindex(new_index)

    # 计算整体IC数值
    if not period:
        ic_data = {}
        for instrument_id in x_df.columns:
            x_series = x_df[instrument_id]
            y_series = y_df[instrument_id]
            ic, _ = pearsonr(x_series, y_series)
            ic_data[instrument_id] = ic
        return Series(ic_data)
    
    # 计算滚动IC数值
    else:
        ic_data = defaultdict(list)

        for instrument_id in x_df.columns:
            x_series = x_df[instrument_id]
            y_series = y_df[instrument_id]

            for x_array, y_array in zip(
                x_series.rolling(period),
                y_series.rolling(period)
            ):
                if len(x_array) < period:
                    ic = 0
                else:
                    ic, _ = pearsonr(x_array, y_array)
                ic_data[instrument_id].append(ic)

        return DataFrame(ic_data, index=new_index)


def calculate_ic_result(ic_series: Series):
    """IC值的的统计指标"""
    ic_mean = ic_series.mean()
    ic_std = ic_series.std()

    if not ic_std:
        ic_ir = 0
        ic_t = 0
    else:
        ic_ir = ic_mean / ic_std
        ic_t, _ = ttest_1samp(ic_series, 0)

    result = {
        "IC_Mean": round(ic_mean, 3),
        "IC_Std": round(ic_std, 3),
        "IC_IR": round(ic_ir, 3),
        "T_Stat": round(ic_t, 3)
    }
    return result

def calculate_factor_sumerize(factor_name, factor_df, return_df):

    # 截面因子数值IC
    normal_series = calculate_cross_section_ic(factor_df, return_df)
    normal_result = calculate_ic_result(normal_series)

    # 截面因子排序IC
    rank_series = calculate_cross_section_ic(factor_df, return_df, True)
    rank_result = calculate_ic_result(rank_series)

    # 时序因子数值IC
    time_series = calculate_time_series_ic(factor_df, return_df)
    time_result = calculate_ic_result(time_series)
    
    result = {
        "name": factor_name,
        # "normal_series": normal_series,
        "normal_result": normal_result,
        # "rank_series": rank_series,
        "rank_result": rank_result,
        # "time_series": time_series,
        "time_result": time_result
    }
    return result

class FactorReport:
    def __init__(self, ctx):
        self.ctx = ctx
        self.factor_datas = defaultdict(list)
        self.price_datas = defaultdict(list)
        self.price_cache = {}


def on_write_synthetic_data(ctx, synthetic_data: lf.types.SyntheticData):
    global factor_report
    # ctx.log.info("on synthetic_data={}, at={}".format(synthetic_data, kft.strftime(ctx.now())))
    factor_report.factor_datas[synthetic_data.key].append(json.loads(synthetic_data.value))
    factor_report.price_datas[synthetic_data.key].append(copy(factor_report.price_cache))

def init(ctx):
    global factor_report
    ctx.log.debug(f"report init")

    factor_report = FactorReport(ctx)


def on_quote(ctx, quote: lf.types.Quote):
    global factor_report
    factor_report.price_cache[f"{quote.instrument_id}.{quote.exchange_id}"] = (quote.ask_price[0] + quote.bid_price[0]) / 2
    # ctx.log.info("on quote={}, at={}".format(quote, kft.strftime(ctx.now())))

def sumerize(ctx) -> Text:
    global factor_report
    ctx.log.debug(f"sumerize")
    for factor_name, data in factor_report.factor_datas.items():
        factor_df = DataFrame.from_dict(data)
        price_df = DataFrame.from_dict(factor_report.price_datas[factor_name])
        return_df = (price_df.shift(-1) - price_df) / price_df
        print(factor_df)
        print(return_df)
        result = calculate_factor_sumerize(factor_name, factor_df, return_df)
        print(result, "\n")

    return {}
