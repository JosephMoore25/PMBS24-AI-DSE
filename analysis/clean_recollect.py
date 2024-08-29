import numpy as np
import pandas as pd
import os
from sklearn.model_selection import train_test_split
from sklearn import svm
from sklearn import multioutput
from sklearn import metrics
from sklearn import linear_model
import joblib
from sklearn.model_selection import GridSearchCV
from sklearn.preprocessing import MinMaxScaler
from sklearn.preprocessing import RobustScaler
from sklearn.preprocessing import StandardScaler
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.preprocessing import PolynomialFeatures
import math
import time
from sklearn.tree import DecisionTreeRegressor
import csv


curdir = "C:/Users/Joseph/Documents/simeng-parameter-study/analysis"
#data = "aarch64-results.csv"
data = "recollect-results.csv"
data_path = os.path.join(curdir, data)

df = pd.read_csv(data_path)

col_str = "cloverleaf_branch_executed,cloverleaf_branch_mispredict,cloverleaf_branch_missrate,cloverleaf_cycles,cloverleaf_decode_earlyFlushes,cloverleaf_dispatch_rsStalls,cloverleaf_fetch_branchStalls,cloverleaf_flushes,cloverleaf_ipc,cloverleaf_issue_backendStalls,cloverleaf_issue_frontendStalls,cloverleaf_issue_portBusyStalls,cloverleaf_lsq_loadViolations,cloverleaf_rename_allocationStalls,cloverleaf_rename_lqStalls,cloverleaf_rename_robStalls,cloverleaf_rename_sqStalls,cloverleaf_retired"
original_cols = col_str.split(",")

new_cols = [str(i) for i in range(0, 18)]

for index, row in df.iterrows():
    if not np.isnan(row[new_cols[0]]):
        for i in range(len(original_cols)):
            if (row[original_cols[i]] != row[new_cols[i]]):
                print("HERE!!!!")
            row[original_cols[i]] = row[new_cols[i]]



df = df.drop(new_cols, axis=1)
print(df.shape)

#df.to_csv('recollect-results.csv', index=False)