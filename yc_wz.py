import scipy.stats as ss
import numpy as np
import pandas as pd
from config import cnf
from db_sql import db_sql

class fake():
    def __init__(self, df, size = 20000) -> None:
        self.df = df
        self.size = size      #伪造的异常数据量大小
        self.start_time = '2022-12-07 03:00:00'
        self.end_time = '2022-12-07 04:00:00'
    
    #获取正态分布的数据
    def get_normal(self):
        x=np.arange(0,60)
        y=ss.norm.pdf(x,loc=30,scale=10)
        y=y/y.sum()
        mi = np.random.choice(x, size = self.size, p = y)
        sen = np.random.choice(x, size = self.size, p = y)
        
        return mi, sen
    
    #时间上的异常
    def get_fakedf(self):
        wz = self.df.sample(self.size)
        mi, sen = self.get_normal()
        hptime = []
        for i in range(self.size):
            tm = self.start_time.split(':')[0]+':'+str(mi[i])+':'+str(sen[i])
            hptime.append(tm)
        wz['happenTime'] = hptime
        wz['happenTime'] = pd.to_datetime(wz['happenTime'])
        return wz
    
    #srcip、dbUser、operType异常
    def get_qtfk1(self):
        wz = self.df.sample(self.size)
        wz['srcIp'] = ['172.24.4.13']*self.size
        wz['dbUser'] = ['kill']*self.size
        # ip_lb = ['172.4.15.8', '142.51.2.21', '171.24.58.33', '185.24.96.39', '163.54.34.5', '156.2.63.4', '155.33.2.85', '151.2.64.9', '196.35.68.2']
        # ur_lb = ['tzy', 'jlp', 'gwb','sjl', 'zsy', 'lt', 'lyb', 'sjb', 'lmx']
        # ii=0
        # for i,j in zip(ip_lb, ur_lb):
        #     self.df.iloc[ii:ii+45000,1] = i
        #     self.df.iloc[ii:ii+45000,11] = j
        #     ii+=45000
        # print(self.df.head())
        return wz
    def get_qtfk2(self):
        wz = self.df.sample(self.size)
        wz['dbUser'] = ['kill']*self.size
        # wz1 = self.df.sample(self.size*100)
        # wz1['dbUser'] = ['tzy']*(self.size*100)
        # wz2 = self.df.sample(self.size*100)
        # wz2['dbUser'] = ['jlp']*(self.size*100)
        # wz3 = self.df.sample(self.size*100)
        # wz3['dbUser'] = ['gwb']*(self.size*100)
        # return pd.concat([wz,wz1,wz2,wz3])
        return wz
    def get_qtfk3(self):
        wz = self.df.sample(self.size)
        wz['operType'] = ['truncate', 'drop']*(self.size//2) + ['drop']*(self.size%2)
        return wz
       
if __name__ == '__main__':
    cnf = cnf()
    db_sql = db_sql(cnf)
    db_sql.cli_ckdb()
    df = db_sql.ck_get()
    
    # df = pd.read_csv('tt.csv')
    # df = df.iloc[:1000]
    fk = fake(df, size=100)
    # wz = fk.get_qtfk()
    wz = fk.get_fakedf()
    df = pd.concat([df,wz])
    print(len(df))
    df.reset_index(drop=True, inplace=True)
    df.to_csv('tt2.csv')
    
    # df['happenTime'] = pd.to_datetime(df['happenTime'])
    # def clsj(ca):
    #         return ca.hour*60+ca.minute
    # df['time_hm'] = df['happenTime'].apply(clsj)
    
    # from count import Count
    # ct = Count(df)
    # ct.tim_plt() 
    