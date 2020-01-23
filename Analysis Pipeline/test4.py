import pandas as pd

#import data as dataFrame
df_user = pd.read_table("sample_file.txt")
df_home = pd.read_csv("kin_sub_final.csv")

df_user['Position'] = ''
df_user['Position'] = df_user.Substrate.str.split("(", n=1, expand = True)[1].str.replace(")", "")
df_user['Substrate'] = df_user.Substrate.str.split("(", n=1, expand = True)[0]

print(df_user)

