对审计到的相关数据库操作信息进行孤立森林的异常分析，然后同过聚类算法进一步对异常进行聚类，方便后续人员进行异常分析

介绍：

    该项目通过从clickhouse数据库读取审计记录，进行一系列的算法、统计分析可视化和异常数据的伪造；
    各个模块对应功能与实现详见下面各模块功能；
    目前没有考虑分批处理，故数据量按电脑资源确定，不宜过大；
    
各模块功能：

    config.py：配置数据库信息、sql执行条件、算法参数
    db_sql.py：数据库连接、sql语句执行、获取datafrane格式数据
    sjcl.py：数据预处理
    model.py：模型算法的学习预测
    main.py：从数据库按条件获取数据进行算法分析

    count.py：统计分析
    flow.py：单独统计时间上的流量
    yc_wz.py：异常数据的伪造
