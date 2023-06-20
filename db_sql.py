from clickhouse_sqlalchemy import make_session
from sqlalchemy import create_engine
import mysql.connector
import pandas as pd

class db_sql():
    def __init__(self, cnf) -> None:
        self.cnf = cnf
        self.ck_session = None
        self.my_session = None

    #连接ck数据库
    def cli_ckdb(self):
        connection = 'clickhouse://{user}:{password}@{server_host}:{port}/{db}'.format(**self.cnf.click_conf)
        engine = create_engine(connection, pool_size=100, pool_recycle=3600, pool_timeout=20)
        self.ck_session = make_session(engine)
    
    #连接mysql数据库
    def cli_mydb(self):
        try:
            self.my_session = mysql.connector.connect(**cnf.mysql_conf)
        except Exception as e:
            print('mysql数据库连接失败：',e)
    
    #从mysql获取信息
    def mysql_get(self, sql=None, Id=None):
        se = self.my_session.cursor()
        if sql:
            se.execute(sql)
        elif Id:   #给到模板id，查询对应的模板语句
            se.execute("SELECT template FROM {0} where id='{1}'".format(cnf.mysql_table_name, Id))
        else:   #查询该表共多少条
            se.execute("SELECT count(1) FROM {0}".format(cnf.mysql_table_name))
        return  se.fetchall()
    
    #从clickhouse获取信息     控制条件：起止时间、数据库类型、目标ip、limit索引                               #自由sql
    def ck_get(self, ij=0,bs=None, count=False, strat_time=None,end_time=None,  dbType=None,destIp=None,  sql=None):
        cnf = self.cnf
        if not strat_time:
            strat_time=cnf.strat_time
        if not end_time:
            end_time=cnf.end_time
        if not dbType:
            dbType=cnf.dbType   

        #计数信息
        if count:
            sql = "SELECT count(1) FROM audit_record WHERE dbType={0} and happenTime BETWEEN '{1}' and '{2}'".format(dbType,strat_time,end_time)
            # cursor = session.execute("SELECT count(1) FROM offline_audit_record WHERE happenTime BETWEEN '{0}' and '{1}'".format(strat_time,end_time))
        
        #表格信息
        elif not sql and strat_time and end_time and dbType:
            if destIp==True:
                #统计当前保护对象类型每个目标IP的计数字典
                sql = '''SELECT destIp,count(1) FROM audit_record WHERE dbType={0} and happenTime BETWEEN'{1}' 
                            and '{2}' GROUP BY destIp ORDER BY count(1)'''.format(dbType,strat_time,end_time)
            elif bs :
                sql = '''SELECT {0} FROM audit_record WHERE dbType={1} and happenTime BETWEEN '{2}' and '{3}' 
                            limit {4},{5}'''.format(cnf.main_tz+cnf.tz[dbType], dbType, strat_time, end_time, ij, bs)
                if destIp:
                    sql = '''SELECT {0} FROM audit_record WHERE destIp='{1}' and dbType={2} and happenTime BETWEEN '{3}' and '{4}' 
                                limit {5},{6}'''.format(cnf.main_tz+cnf.tz[dbType], destIp, dbType, strat_time, end_time, ij, bs)
            else:
                sql = '''SELECT {0} FROM audit_record WHERE dbType={1} and happenTime BETWEEN '{2}' 
                            and '{3}' '''.format(cnf.main_tz+cnf.tz[dbType], dbType, strat_time, end_time)
                
                if destIp:
                    sql = '''SELECT {0} FROM audit_record WHERE destIp='{1}' and dbType={2} and happenTime BETWEEN '{3}' 
                                and '{4}' '''.format(cnf.main_tz+cnf.tz[dbType], destIp, dbType, strat_time, end_time)
        
        if sql:
            try:
                cursor = self.ck_session.execute(sql)
                fields = cursor._metadata.keys
                df = pd.DataFrame([dict(zip(fields, item)) for item in cursor.fetchall()])
                # return cursor.fetchall()
                return df
            except Exception as e:
                raise(e)
        
        else:
            return '执行sql语句为空或sql必要条件为空'
        
if __name__ == '__main__':
    from config import cnf
    cnf=cnf()
    db_sql=db_sql(cnf)
    
    # db_sql.cli_mydb()
    db_sql.cli_ckdb()
    
    # js = db_sql.mysql_get(Id='7176854313362588233')
    # js = db_sql.ck_get(sql = "SELECT * FROM audit_record where destIp='172.23.1.21' limit 10")
    # js = db_sql.ck_get(sql = "SELECT count(1) FROM audit_record where destIp='172.23.1.21' ")
    
    js = db_sql.ck_get()
    print(js.nunique())
    # print(js)