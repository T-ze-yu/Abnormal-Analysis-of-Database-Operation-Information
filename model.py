from pyod.models.iforest import IForest
import numpy as np
from sklearn.cluster import DBSCAN
from collections import Counter

class model():
    def __init__(self, clf=None, cnf=None) -> None:
        self.clf = clf
        self.cnf = cnf
        
    def learn(self, df):
        self.clf = IForest(random_state=self.cnf.ra_state, n_estimators=self.cnf.n_est, max_samples=self.cnf.max_samples, n_jobs=-1).fit(df)
        
    def predict(self, df):
        if self.clf:
            lb=self.clf.predict_proba(df)[:,1]
            #找到超过阈值的真值表并保存
            sy_lb = np.where(lb > self.cnf.yz, True, False)
            df = df[list(sy_lb)]
            return sy_lb, df
    
    def cluster(self, df):
        clustering = DBSCAN(eps=self.cnf.eps, min_samples=self.cnf.min_samples).fit(df)
        return clustering.labels_+1
    
    
    
    