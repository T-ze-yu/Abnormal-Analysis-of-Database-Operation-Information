from sjcl import process
from model import model
import os
import joblib

def main():
    from config import cnf
    from db_sql import db_sql
    
    if not os.path.exists('res'):
        os.mkdir('res')
        os.mkdir('res/model')    
        os.mkdir('res/pic')    

    #加载配置文件
    cnf = cnf()
    cnf.get_cs()      #获取算法参数
    
    #连接数据库，获取数据
    db_sql = db_sql(cnf)
    db_sql.cli_ckdb()
    df = db_sql.ck_get()
    
    #数据预处理
    pro = process(cnf.count_cols, cnf.one_hot_cols, cnf.label_cols)
    pro.get_df(df.copy())
    pro.process_data()
    
    #模型学习与预测
    md = model(cnf=cnf)
    md.learn(pro.df)
    sy_lb, df_yc1 = md.predict(pro.df)
    jl_bq = md.cluster(df_yc1)     #聚类分析
    df = df[list(sy_lb)]
    df['clustering'] = jl_bq
    df.to_csv('res/yc_res.csv',index=False,encoding='utf-8')
    joblib.dump(md.clf, 'res/model/'+'model.pkl')
    
    
if __name__ == '__main__':
    main()
    
    


