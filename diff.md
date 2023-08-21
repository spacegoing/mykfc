
1. 使用版本为v2.6.1-alpha.4 https://github.com/kungfu-trader/kungfu/pull/1017
1. 数据准备工具过去时 kfc tool， 如今是 kfc slicetool  新增参数 --indexer_path ./month_indexer.py 用于指定数据索引器的位置，从而控制数据生成的分片机制。
1. 数据准备（slicetool执行的结果）完成后会放置在 {KF_HOME)/home/dataset 下，可以通过修改 month_indexer.py 来指定数据的位置， 从而控制数据读取的分片机制。
1. 运行策略时的命令 相比过去增加了 --from_indexer ./month_indexer.py 参数，用于指定数据索引器的位置, 从而控制数据生成的分片机制
1. 运行python策略的方式。kfc  -l info run  ./py_stg.py -M ./matcher-example/dist/KungfuSimpleMatcher/KungfuSimpleMatcher.cpython-39-x86_64-linux-gnu.so --from_indexer ./month_indexer.py -c strategy -m backtest -b 20200102 -e 2021-01-02 -g custom-test -n custom-test
1. 新增算子 operator回测。 可以订阅依赖后生成 合成数据供其他 策略或算子回测使用， 合成数据的存储位置由 month_indexer.py 来指定。