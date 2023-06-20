
from collections import Counter
import matplotlib.pyplot as plt
import pandas as pd
from config import cnf
from db_sql import db_sql

# 正确显示中文和负号
plt.rcParams["font.sans-serif"] = ["SimHei"]
plt.rcParams["axes.unicode_minus"] = False

#在所有字段中只有time_hms（时分秒是连续特征）可以使用均值和分布
class Count():
    def __init__(self,cl_data,yc_data=None) -> None:
        self.cl_data=cl_data
        self.yc_data=yc_data
        self.sum=len(cl_data)
        self.alldc = {}     #记录整体所有字段计数
    
    def get_alldc(self):
        for cc in self.cl_data.columns:
            if cc!= 'operSentence' and cc!= 'happenTime':
                self.alldc.update({cc:Counter(self.cl_data[cc].values)})
                
    #计算异常数据中各字段值在整体出现的频率
    def yc_plv(self):
        for cc in self.cl_data.columns:
            if cc!= 'operSentence' and cc!= 'happenTime' and 'time_hm':
                ycdic = Counter(self.yc_data[cc].values)
                ln = len(ycdic)
                ycln = len(self.yc_data)
                aln = len(self.cl_data)
                
                width=0.3
                plt.bar([i for i in range(ln)], [self.alldc[cc][i]/aln for i in ycdic.keys()], width=width, label='整体')
                plt.bar([i+width for i in range(ln)], [i/ycln for i in ycdic.values()], width=width, label='异常')
                if len(ycdic.keys())>20:
                    plt.xticks([x+width/2 for x in range(ln)], ycdic.keys(), rotation = 75)
                else:
                    plt.xticks([x+width/2 for x in range(ln)], ycdic.keys())
                for a,b in zip(range(ln),ycdic.keys()):   #柱子上的数字显示
                    b2 = ycdic[b]/ycln
                    b1 = self.alldc[cc][b]/aln
                    plt.text(a,b1,'%.4f'%b1,ha='center',va='bottom',fontsize=10)
                    # plt.text(a,b1,b1,ha='center',va='bottom',fontsize=15)
                    plt.text(a+width,b2,'%.4f'%b2,ha='center',va='bottom',fontsize=10)
                    # plt.text(a+width,b2,b2,ha='center',va='bottom',fontsize=15)
                plt.legend()
                plt.suptitle(cc, fontsize=30)
                plt.savefig('res/pic/'+cc+".png",dpi=1000)
                plt.show()        
                
    def shw(self, js, tm):
        c=0
        for i in range(len(js)):
            if int(js[c][0])==i+int(js[0][0]):
                plt.bar(i+int(js[0][0]),js[i][1])
                c+=1
            else:
                plt.bar(i+int(js[0][0]),0)
        # plt.bar([i[0] for i in js], [i[1] for i in js])
        # 设置图片名称
        plt.suptitle(tm)
        # 设置x轴标签名
        plt.xlabel("时间（单位：分）")
        # 设置y轴标签名
        plt.ylabel("次数")
        plt.savefig('res/pic/'+tm+".png",dpi=1000)
        plt.show()
    
    #画出时分的时间分布图
    def tim_plt(self, dif=False):
        if dif and self.yc_data.bool:
            ycdic = Counter(self.yc_data['time_hm'].values)
            ycdic = sorted(ycdic.items(), key=lambda x: x[0])
            self.shw(ycdic, '异常数据的时间分布')
            
        cdic = Counter(self.cl_data['time_hm'].values)
        cdic = sorted(cdic.items(), key=lambda x: x[0])
        self.shw(cdic, '正常数据的时间分布')
        
#分析思路：对比整体和异常的时间分布差异、对比整体稀值和异常众数的重合度
if __name__ == '__main__':
    cnf = cnf()
    db_sql = db_sql(cnf)
    db_sql.cli_ckdb()
    df = db_sql.ck_get()
    
    # print(len(df))
    # df = df.sample(100000)
    # print(len(df))
    #添加伪造的异常数据
    # from yc_wz import fake
    # fk = fake(df, 4000)
    # wz = fk.get_fakedf()
    # df = pd.concat([df,wz])
    # df.reset_index(drop=True, inplace=True)
    # df = pd.read_csv('ys_wz.csv')
    
    df_yc = pd.read_csv('res/yc_res.csv')
    df_yc['happenTime'] = pd.to_datetime(df_yc['happenTime'])
    def clsj(ca):
        # return str(ca.hour)+':'+str(ca.minute)
        return ca.hour*60+ca.minute
    df_yc['time_hm'] = df_yc['happenTime'].apply(clsj)
    
    df['time_hm'] = df['happenTime'].apply(clsj)
    
    #在实例化该类，统计时间分布和值频率分布
    ct = Count(df, df_yc)
    ct.get_alldc()
    ct.tim_plt(dif=True) 
    ct.yc_plv() 
    
    