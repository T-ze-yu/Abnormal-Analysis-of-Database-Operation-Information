# 审计对象  ip
# 时间范围

class cnf():
    def __init__(self) -> None:
        #数据库连接信息
        self.click_conf = {
                "user": "root",
                "password": "Ankki_cK123",
                "server_host": "172.24.4.85",
                "port": "8123",
                "db": "bs_audit",
                "tabel": "audit_record"
            }
        self.mysql_conf = {
                "user": "root",
                "password": "Ankki_mySQL123",
                "host": "172.24.4.85",
                # "port": "3306",
                "db": "bs_audit"
            }
        self.mysql_table_name = 'sql_template_record'
        
        #查询语句条件信息
        self.strat_time = '2022-12-07 00:00:00'
        self.end_time = '2022-12-07 23:59:59' 
        self.dbType = 40             #2
        self.destIp = None        #178262108
        
        #数据处理信息     主要特征字段
        self.main_tz = 'happenTime,srcIp,srcPort,destIp,destPort,sessionId,operType,operSentence,'
        #各类数据库特有字段
        self.tz={
            2:'tableName',
            40:'tableName,fieldName,sqlTemplateId,dbUser'          
        }
        #各字段处理方式
        self.count_cols = {}            #使用频率编码的字段  
        self.one_hot_cols = {'dbUser'}          #使用独热编码的字段  建议该字段的值取集合后长度较短，防止维度爆炸
        self.label_cols = {'tableName','fieldName','sqlTemplateId', 'operType',        'sessionId', 'destPort','srcPort'}            #使用标签编码的字段
    
    #算法参数信息     
    def get_cs(self):
        self.bs = 60000   #分批读数据批的大小
        self.frac = 0.8   #每次从当前批取样的比例
        self.cs = 4       #每批增量学习和数据预测的次数
        self.n_est = 20   #每次学习生成的树的颗数
        
        self.ra_state = 666      #随机种子
        self.max_samples = 256   #随机抽取的每颗树的学习样本数
        self.yz = 0.9    #判断异常的阈值
        self.eps=100     #聚类的最短半径
        self.min_samples=50         #聚类的最少个数
        

'''72--redis
49--Mong0DB
2--MySQL
7--PostgreSQL
83--Es
40--MariaDB
'''