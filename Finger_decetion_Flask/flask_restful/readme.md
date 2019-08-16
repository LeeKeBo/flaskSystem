app 就是主要的应用模块啦

client.py 是个测试api模块的客户端程序

config.py 是配置信息所在处，这里可能归类不好，待修改

db_create.py 用来生成数据库的，但是这里的生成会导致原本的数据全部丢失。。。


下面的都未实现：

db_downgrade, db_upgrade, db_migrate 分别用于数据库的升级， 降级， 迁移， 可能是生成数据库脚本的形式，尽量保留原有数据

migrations  这里应该存放数据库版本的，以及些数据库脚本

tests 应当是用来写测试Web的脚本的，来测试每个模块的功能

venv 应当表明实验的环境之类的


