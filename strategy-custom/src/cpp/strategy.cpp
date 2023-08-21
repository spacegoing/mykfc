#include <kungfu/wingchun/extension.h>
#include <kungfu/wingchun/strategy/context.h>
#include <kungfu/wingchun/strategy/strategy.h>
#include <kungfu/yijinjing/journal/assemble.h>

using namespace kungfu::longfist::enums;
using namespace kungfu::longfist::types;
using namespace kungfu::wingchun::strategy;
using namespace kungfu::wingchun::strategy;
using namespace kungfu::yijinjing::data;
using kungfu::event_ptr;
int i = 0;
KUNGFU_MAIN_STRATEGY(KungfuStrategyCustom) {
public:
  KungfuStrategyCustom() = default;
  ~KungfuStrategyCustom() = default;

  void pre_start(Context_ptr & context) override {
    SPDLOG_INFO("preparing strategy");
    context->add_account("custom", "123456");
    SPDLOG_INFO("nowL: {}", context->now());

    // context->add_timer(context->now() + 1000000000000000000,
    //                    [=](auto e) { context->subscribe("custom", {"CF202005", "sc202212"}, {EXCHANGE_SHFE}); });
    context->subscribe("custom", {"CF202005", "sc202212"}, EXCHANGE_SHFE);

    context->subscribe_operator("custom-op", "custom-op");
    // context->subscribe_operator("bar", "my-bar");
  }

  void post_start(Context_ptr & context) override { SPDLOG_INFO("strategy started"); }

  void post_stop(Context_ptr & context) override { SPDLOG_INFO("strategy stopped"); };

  void on_synthetic_data(Context_ptr & context, const SyntheticData &synthetic_data, const location_ptr &location,
                         uint32_t dest) override {
    SPDLOG_INFO("on_synthetic_data: {} ", synthetic_data.to_string());
  }

  void on_quote(Context_ptr & context, const Quote &quote, const location_ptr &location, uint32_t dest) override {
    SPDLOG_INFO("on quote: {} ", quote.to_string());
    auto now = context->now();
    context->add_timer(context->now() + 1000000000, [=](const event_ptr & event) {
      SPDLOG_INFO("timer called at: {}, duration={}", context->now(), (context->now() - now));
    });
    // context->insert_order(quote.instrument_id, quote.exchange_id, "SSE", "123456", quote.ask_price[0] + 5, 100,
    //                       PriceType::Limit, Side::ShortSell, Offset::Open);
    context->insert_order(quote.instrument_id, quote.exchange_id, "custom", "123456", quote.bid_price[0] + 5, 100,
                          PriceType::Limit, Side::Buy, Offset::Open);
  }

  void on_entrust(Context_ptr & context, const Entrust &entrust, const location_ptr &location, uint32_t dest) {}

  void on_transaction(Context_ptr & context, const Transaction &transaction, const location_ptr &location,
                      uint32_t dest) {}

  void on_order(Context_ptr & context, const Order &order, const location_ptr &location, uint32_t dest) override {
    // SPDLOG_INFO("on order: {} location->name {}", order.to_string(), location->uname);
  }

  void on_trade(Context_ptr & context, const Trade &trade, const location_ptr &location, uint32_t dest) override {
    // SPDLOG_INFO("on trade: {} location->name {}", trade.to_string(), location->uname);
  }
};
