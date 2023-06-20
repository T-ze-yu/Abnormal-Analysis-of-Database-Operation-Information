#对目标ip分组统计  可视化   超参数调整级数分组
from config import cnf
from db_sql import db_sql

cnf=cnf()
db_sql=db_sql(cnf)

db_sql.cli_ckdb()
df = db_sql.ck_get(destIp=True)

print(df)



#根据各个ip的数量进行分组
def ip_group(df):
    sum=0
    ip_lb=[]
    ip=[]
    for i in df.values:
        sum+=int(i[1])
        ip.append(i[0])
        if 500000<sum:
            sum=0
            ip_lb.append(ip)
            ip=[]
    return ip_lb