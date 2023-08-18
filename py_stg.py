import random
import csv
from kungfu.wingchun.constants import *
import kungfu.yijinjing.time as kft

source = "custom"
account = "123456"
exchange = Exchange.SHFE


def pre_start(context):

    context.log.info("preparing strategy")

    context.subscribe(source, ["CF202005", "sc202212"], Exchange.SHFE)
    context.add_account(source, account)
    context.subscribe_operator("custom-op", "custom-op")


def on_quote(context, quote, location, dest):
    now = context.now()
    context.add_timer(context.now()+ 10 * kft.NANO_PER_SECOND, lambda ctx, time_event: context.log.info("timer set={}, print now={}, duration={}s".format(now, ctx.now(), (ctx.now() - now) / kft.NANO_PER_SECOND)))
    side = random.choice([Side.Buy, Side.Sell])
    side = Side.Buy
    price = quote.ask_price[0] if side == Side.Buy else quote.bid_price[0]
    price_type = random.choice([PriceType.Any, PriceType.Limit])
    context.insert_order(quote.instrument_id, quote.exchange_id, source, account, quote.bid_price[0] + 5, 100,
                          PriceType.Limit, Side.Buy, Offset.Open)
    pass


def on_order(context, order, location, dest):
    # context.log.info("order: {}".format(order))
    pass

def on_trade(context, trade, location, dest):
    context.log.info("trade: {}".format(trade))
    pass

