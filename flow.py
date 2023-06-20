
from db_sql import db_sql
from config import cnf
import pandas as pd
from collections import Counter

def get_flow_dfs(fk=False):
    flow_dfs = pd.DataFrame()
    for d in range(9,10):
        if d<10:
            d='0'+str(d)
        else:
            d=str(d)
        strat_time = '2022-12-'+d+' 00:00:00'
        end_time = '2022-12-'+d+' 23:59:59'
        df = db_sql.ck_get(sql = "SELECT happenTime FROM audit_record WHERE dbType=40 and happenTime BETWEEN '{0}' and '{1}'".format(strat_time,end_time))
        df = pd.DataFrame(df).sample(10000)
    
        def clsj(ca):
            return ca.hour*60+ca.minute
        
        df['time_hm'] = df['happenTime'].apply(clsj)
        cu = Counter(df['time_hm'].values)
        cu = sorted(cu.items(), key=lambda x: x[0])
        
        flow_df = pd.DataFrame()
        flow_df['time_hm'] = [i[0] for i in cu]
        flow_df['size']  = [i[1] for i in cu]
        flow_dfs = flow_dfs.append(flow_df)
        
    return flow_dfs

if __name__ == '__main__':
    cnf = cnf()
    cnf.get_cs()
    db_sql = db_sql(cnf)
    db_sql.cli_ckdb()
    
    flow_dfs = get_flow_dfs(fk=True)
    print(len(flow_dfs))
    flow_dfs.to_csv('fw.csv')
           
                            