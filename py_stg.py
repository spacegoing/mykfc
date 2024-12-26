import random
import csv, time
from kungfu.wingchun.constants import *
import kungfu.yijinjing.time as kft

source = "custom"
account = "123456"
exchange = Exchange.SSE
stock_list = ["600030"]


def pre_start(context):
    context.log.info("preparing strategy")
    context.subscribe(source, stock_list, exchange)
    context.add_account(source, account)
    context.n = 1


def on_quote(context, quote, location, dest):
    context.order_id = context.insert_order(
        quote.instrument_id,
        quote.exchange_id,
        source,
        account,
        quote.last_price,
        200,
        PriceType.Limit,
        Side.Buy,
        Offset.Open,
    )

    context.log.info("context.order_id : {}".format(context.order_id))


def on_entrust(context, entrust, location, dest):
    context.log.info("[on_entrust] {}".format(entrust))


def on_transaction(context, transaction, location, dest):
    context.log.info("[on_transaction] {}".format(transaction))


def on_order(context, order, location, dest):
    context.log.warning("order: {}".format(order))


def on_trade(context, trade, location, dest):
    context.log.warning("trade: {}".format(trade))


def post_stop(context):
    book = context.book
    long_positions = list(book.long_positions.values())
    short_positions = list(book.short_positions.values())
    # print("trades: \n", list(book.trades.items()))
    print("long_positions:\n", long_positions)
    print("short_positions:\n", short_positions)
