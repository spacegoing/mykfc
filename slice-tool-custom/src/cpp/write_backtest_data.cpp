
#include <fstream>
#include <iostream>
#include <kungfu/wingchun/extension.h>
#include <kungfu/wingchun/tool/sliceindexer.h>
#include <kungfu/wingchun/tool/slicetool.h>
#include <kungfu/yijinjing/common.h>
#include <kungfu/wingchun/common.h>
#include <spdlog/spdlog.h>
#include <filesystem>
#include <sstream>
#include <string>
#include <vector>

using namespace kungfu::longfist::enums;
using namespace kungfu::longfist::types;
using namespace kungfu::yijinjing::data;
using namespace kungfu::wingchun::tool;
using kungfu::yijinjing::time;
namespace fs = std::filesystem;

KUNGFU_MAIN_SLICE_TOOL(TestCustomSliceTool)
{
public:
  const int logInterval = 10000;
  using SliceTool::SliceTool;
  virtual void run() override
  {
    kungfu::yijinjing::journal::frame_ptr frame;

    fs::path csv_path(get_arguments());
    if (not fs::exists(csv_path))
    {
      spdlog::error("csv file: {} not exist", csv_path.string());
      return;
    }
    std::ifstream csvData(csv_path.string());
    std::string line;
    std::vector<std::vector<std::string>> parsedCsv;
    std::unordered_map<std::string, std::string> product_exchange_map;
    std::ifstream input_json_file("backtest_config.json");
    nlohmann::json config_json;
    input_json_file >> config_json;
    for (auto& x : config_json["Commission"]["default"]) {
      product_exchange_map.emplace(x["product_id"], x["exchange_id"]);
    }
    // spdlog::info("product_exchange_map {}", product_exchange_map["AU"]);

    for (int i = 0; std::getline(csvData, line); ++i)
    {
      std::istringstream csvStream(line);
      std::string cell;
      std::vector<std::string> parsedRow;

      while (std::getline(csvStream, cell, ','))
      {
        parsedRow.push_back(cell);
      }
      if (i == 0)
      {
        continue;
      }

      uint64_t dsTime = std::stoull(parsedRow[1]);
      uint64_t rvTime = std::stoull(parsedRow[2]);
      double ask = std::stod(parsedRow[3]);
      double bid = std::stod(parsedRow[4]);
      double lastPrice = std::stod(parsedRow[5]);
      double vwapPrice = std::stod(parsedRow[6]);
      int askVolume = std::stoi(parsedRow[7]);
      int bidVolume = std::stoi(parsedRow[8]);
      int volume = std::stoi(parsedRow[9]);
      int openInterest = std::stoi(parsedRow[10]);
      std::string instrumentID = parsedRow[11];

      Quote quote{};
      quote.instrument_id = instrumentID.c_str();
      quote.exchange_id = product_exchange_map[get_product_id(instrumentID)].c_str();
      quote.ask_price[0] = ask;
      quote.bid_price[0] = bid;
      quote.ask_volume[0] = askVolume;
      quote.bid_volume[0] = bidVolume;
      quote.open_interest = openInterest;
      quote.data_time = dsTime;
      quote.last_price = lastPrice;
      quote.volume = volume;
      quote.instrument_type = InstrumentType::Future;
      ////!! 写入数据的相关接口
      // 写入数据 , 注意 第一个参数为数据首包本地时间戳， 第二个参数为 数据落盘本地时间戳。 后者严格 大于等于前者。
      write_at(rvTime, rvTime, location::PUBLIC, quote);

      if (i % logInterval == 0) {
        spdlog::info("{} rows written", i);
      }

      ////!! 两个读取数据的相关接口
      // 取到 刚写入的 一帧数据。
      frame = current_frame();
      // 根据帧数据的类型字段，对无类型数据做一次类型转换。
      if (frame->msg_type() != Quote::tag or frame->data<Quote>().to_string() != quote.to_string())
      {
        spdlog::info("the {}th frame: {} not qualified", i, frame->data<Quote>().to_string());
      }
      // cursor移动到下一帧待写入数据的内存区域。
      next();
    }
  }

  std::string get_product_id(std::string instrumentID) {
    std::string product_id;
    for (char c : instrumentID) {
        if (std::isalpha(c)) {
            product_id += std::toupper(c);
        } 
    }
    return product_id;
  }

};
