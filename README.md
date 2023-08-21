# kfx-demo-backtest

### 使用说明

解压缩data-clean/snapshot.zip

```
# 安装
yarn install

# 编译
yarn build
```


#### windows
```
# 准备数据
yarn kfc -l info  slicetool -t .\slice-tool-custom\dist\KungfuSliceToolCustom\KungfuSliceToolCustom.cp39-win_amd64.pyd --indexer_path .\month_indexer.py -c md -g custom -n custom -b 2020-01-02 -e 2021-01-02 --arguments .\data-clean\snapshot.csv

yarn kfc -l info run .\dist\KungfuOperatorCustom\KungfuOperatorCustom.cp39-win_amd64.pyd --from_indexer .\month_indexer.py --to_indexer .\month_indexer.py -c operator -m backtest -b 2020-01-02 -e 2021-01-02 -g custom-op -n custom-op

# cpp策略回测
yarn kfc -l info run .\strategy-custom\dist\KungfuStrategyCustom\KungfuStrategyCustom.cp39-win_amd64.pyd -M .\matcher-example\dist\KungfuSimpleMatcher\KungfuSimpleMatcher.cp39-win_amd64.pyd --from_indexer .\month_indexer.py -c strategy -m backtest -b 2020-01-02 -e 2021-01-02 -g custom-stg -n custom-stg

# py策略回测

yarn kfc -l info run .\py_stg.py -M .\matcher-example\dist\KungfuSimpleMatcher\KungfuSimpleMatcher.cp39-win_amd64.pyd --from_indexer .\month_indexer.py -c strategy -m backtest -b 2020-01-02 -e 2021-01-02 -g custom-stg -n custom-stg

```

#### linux
```

```

