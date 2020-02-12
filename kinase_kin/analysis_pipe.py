import pandas as pd
import numpy as np
import plotly.express as px
import sqlite3


def get_format(filepath):
    df = pd.read_table(filepath)
    drug_num = (len(df.columns) - 2)/5
    if (len(df.columns)-2)%5 != 0:
        return 1
    else:
        return 0


#connecting to the database
def create_df_user(filepath):
    conn = sqlite3.connect("KinaseDatabasev1.db")
    SQL_Query = pd.read_sql_query("SELECT SubstrateInfo.Kinase, SubstrateInfo.Substrate_Symbol,SubstrateInfo.Sub_Gene, SubstrateInfo.Sub_Mod_Rsd FROM SubstrateInfo",conn)

    # import data as dataFrame
    df_user = pd.read_table(filepath)
    df_home = pd.DataFrame(SQL_Query, columns=['Kinase','Substrate_Symbol','Sub_Gene','Sub_Mod_Rsd'])

    # requires CSV uploaded with columns [1] Substrates(Position) [2] control_mean [3] condition_mean [4] FC [5] p_val [6] Any
    df_user['Position'] = ''
    df_user['Position'] = df_user.Substrate.str.split("(", n=1, expand = True)[1].str.replace(")", "")
    df_user['Substrate'] = df_user.Substrate.str.split("(", n=1, expand = True)[0]
    df_user.columns = ('Substrate', 'control_mean2', 'condition_mean3', 'FC4', 'pval5', 'cv_control6', 'cv_condition7', 'Position')

    df_user['FC_log2'] = np.log2(df_user['FC4'])
    print(list(df_user.columns))
    # adds the kinase names to the dataframe with user's data if their is a matching SUB_MOD_RSD and SUB_GENE
    df_user = df_user.join(df_home[["Kinase", "Sub_Gene", "Sub_Mod_Rsd"]].set_index(["Sub_Gene", "Sub_Mod_Rsd"]),
                     on= ['Substrate', 'Position'])

    df_user = df_user.join(df_home[["Kinase", "Substrate_Symbol", "Sub_Mod_Rsd"]].set_index(["Substrate_Symbol", "Sub_Mod_Rsd"]),
                     on= ['Substrate', 'Position'], rsuffix= '_sub_acc')

    #cleaning data, removing Nans, O, infinity
    df_user = df_user.replace([np.inf, -np.inf], np.nan)
    df_user = df_user.dropna()
    df_user = df_user.dropna(axis=0)
    df_user = df_user.dropna(subset = ['Kinase'])
    df_user = df_user[(df_user.FC_log2 != "inf")]
    df_user = df_user[(df_user.FC_log2 != "0")]
    return df_user


#calculating 2 scores
def mean_score(kinase, dataset):
    '''mean of the log2 FC of all phosphosites in the substrate set'''

    sub_set = dataset[dataset['Kinase'] == kinase]
    return sub_set['FC_log2'].mean()


def delta_score(threshold, kinase, dataset):
    '''number of significant positive phosphosite minus
    significant down-regulated sites in each substrate set'''
    sub_set_neg = dataset[(dataset['Kinase'] == kinase) & (dataset['pval5'] < threshold) &
                      (dataset['FC_log2'] < 0)]
    sub_set_pos = dataset[(dataset['Kinase'] == kinase) & (dataset['pval5'] < threshold) &
                          (dataset['FC_log2'] > 0)]
    return len(sub_set_pos)-len(sub_set_neg)










