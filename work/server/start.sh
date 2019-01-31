nohup python -u monitor.py > log/test.log &
nohup python -u swagger_test/monitor_api.py > log/test_api.log &
nohup python -u fxh/feixiaohao_api.py > log/fxh.txt &
nohup python -u fxh/bxx_depth.py > log/market_depth.txt &
nohup python -u fxh/bxx_all_depth.py > log/market_all_depth.txt &
