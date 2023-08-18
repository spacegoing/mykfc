#include <kungfu/wingchun/extension.h>
#include <kungfu/wingchun/operator/context.h>
#include <kungfu/wingchun/operator/operator.h>
#include <kungfu/yijinjing/journal/assemble.h>

using namespace kungfu::longfist::enums;
using namespace kungfu::longfist::types;
using namespace kungfu::wingchun::op;
using namespace kungfu::yijinjing::data;
KUNGFU_MAIN_OPERATOR(KungfuOperatorCustom) {
public:
  void pre_start(Context_ptr & context) override {
    SPDLOG_INFO("preparing operator");
    // context->subscribe("sim", {"test"}, {"Comdty"});
    // context->subscribe("sim", {"600000"}, {"SSE"});
    SPDLOG_INFO("now: {}", context->now());
    context->subscribe("custom", {"CF202005", "sc202212"}, {EXCHANGE_SHFE});
    // context->subscribe_operator("bar", "my-bar");
  }

  void post_start(Context_ptr & context) override { SPDLOG_INFO("operator started"); }

  void on_quote(Context_ptr & context, const Quote &quote, const location_ptr &location, uint32_t dest) override {
    // SPDLOG_INFO("on quote: {} ", quote.to_string());
    context->publish_synthetic_data("last_price", std::to_string(quote.last_price));
  }

};
