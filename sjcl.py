from config import cnf
from db_sql import db_sql
from rich.progress import track
import pandas as pd
import IPy
from category_encoders import OneHotEncoder, CountEncoder

#数据处理的类
class process():
    def __init__(self, count_cols, one_hot_cols, label_cols) -> None:
        self.df = None
        self.label_dict = {}
        self.count_cols = count_cols          
        self.one_hot_cols = one_hot_cols          
        self.label_cols = label_cols  

    #获取datafrom格式的数据
    def get_df(self, df):
        self.df = df
    #将时分秒归一为秒
    def clsj(self, ca):
        return ca.second+ca.minute*60+ca.hour*3600
    #将整数ip转换为分段ip
    def ip_int(self, intip):
        return IPy.intToIp(intip,4)

    #时间的处理
    def time_feature(self):
        if 'happenTime' in self.df.columns:
            # df['happenTime'] = pd.to_datetime(df['happenTime'])
            self.df['time_year'] = self.df['happenTime'].dt.year
            self.df['time_month'] = self.df['happenTime'].dt.month
            self.df['time_day'] = self.df['happenTime'].dt.day
            self.df['time_dow'] = self.df['happenTime'].dt.day_of_week
            self.df['time_hms'] = self.df['happenTime'].apply(self.clsj)
            self.df = self.df.drop(['happenTime'], axis=1)

    #ip的处理
    def ip_feature(self):
        ddf1 = self.df['srcIp'].str.split('.', expand=True)
        ddf1.columns = ['srcip1','srcip2','srcip3','srcip4']
        ddf2 = self.df['destIp'].str.split('.', expand=True)
        ddf2.columns = ['destip1','destip2','destip3','destip4']

        self.df = pd.concat([self.df,ddf1,ddf2], axis=1)
        self.df = self.df.drop(['srcIp'], axis=1)
        self.df = self.df.drop(['destIp'], axis=1)
    
    #频率编码
    def count_encode(self):
        cols = list(set(self.df.columns) & self.count_cols)
        encoder = CountEncoder(cols = cols).fit(self.df)
        self.df = encoder.transform(self.df)
        return encoder

    #独热编码
    def one_hot(self):
        cols = list(set(self.df.columns) & self.one_hot_cols)
        encoder = OneHotEncoder(cols=cols, 
                            handle_unknown='indicator', 
                            handle_missing='indicator', 
                            use_cat_names=True).fit(self.df)
        self.df = encoder.transform(self.df) # 转换训练集
        return encoder

    #使用字典进行label code
    def zdsy(self, tx, dic):
        if tx not in dic.keys():
            dic.update({tx:len(dic)+1})
        return dic[tx]
    #标签编码
    def label_code(self):
        cols = list(set(self.df.columns) & self.label_cols)
        for c in track(cols):
            print('label_code:',c)
            self.df[c]=[ self.zdsy(i, self.label_dict) for i in self.df[c]]
    
    #总的处理函数   
    def process_data(self):
        assert self.df is not None, '数据源为空'
        
        self.time_feature()
        self.ip_feature()
        
        if self.one_hot_cols:
            self.one_hot()
        if self.count_cols:
            self.count_encode()
        if self.label_cols:
            self.label_code()
        self.df.drop('operSentence',axis=1,inplace=True)
        

if __name__=='__main__':
    cnf = cnf()
    db_sql = db_sql(cnf)
    db_sql.cli_ckdb()
    df = db_sql.ck_get()
    
    # print(set(df['operType'].values))
    # print(set(df['dbUser'].values))
    # print(set(df['srcIp'].values))

    pro = process(cnf.count_cols, cnf.one_hot_cols, cnf.label_cols)
    pro.get_df(df)
    pro.process_data()
    print(pro.df.head())
    print(df.head())
    
    # print(pro.df.shape)
    # print(pro.one_hot_cols)
    # print(pro.count_cols)

    
