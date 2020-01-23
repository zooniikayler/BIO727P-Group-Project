import pandas as pd
from collections import Counter
df_asmt = pd.read_csv("kin_sub_final.csv")
#df_refsource = pd.read_csv("refKSI.csv")
#df_razlist = pd.read_csv("KinaseInfo_300.csv")

a = df_asmt['KINASE']
#b = df_refsource['kinase']
#c = df_razlist['Kinase Symbol']
#g = df_refsource['substrate']


print(len(set(a)))

