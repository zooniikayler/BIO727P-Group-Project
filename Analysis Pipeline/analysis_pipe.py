import pandas as pd
import numpy as np
import plotly.express as px

#import data as dataFrame
df_user = pd.read_table("sample_file.txt")
df_home = pd.read_csv("kin_sub_final.csv")


#preparing uploaded data
#requires CSV uploaded with columns [1] Substrates(Position) [2] control_mean [3] condition_mean [4] FC [5] p_val [6] Any


#def prepare_user_data(csv):


df_user['Position'] = ''
df_user['Position'] = df_user.Substrate.str.split("(", n=1, expand = True)[1].str.replace(")", "")
df_user['Substrate'] = df_user.Substrate.str.split("(", n=1, expand = True)[0]

df_user['AZ20_fold_change_log2'] = np.log2(df_user['AZ20_fold_change'])

#adds the kinase names to the dataframe with user's data if their is a matching SUB_MOD_RSD and SUB_GENE
df_user = df_user.join(df_home[["KINASE", "SUB_GENE", "SUB_MOD_RSD"]].set_index(["SUB_GENE", "SUB_MOD_RSD"]),
             on= ['Substrate', 'Position'])

df_home = df_user.join(df_home[["KINASE", "SUB_ACC_ID", "SUB_MOD_RSD"]].set_index(["SUB_ACC_ID", "SUB_MOD_RSD"]),
             on= ['Substrate', 'Position'], rsuffix= '_sub_acc')

#cleaning data, removing Nans, O, infinity
df_user = df_user.dropna()
df_user= df_user.dropna(axis=0)
df_user = df_user.dropna(subset = ['KINASE'])
df_user = df_user[(df_user.AZ20_fold_change_log2 != "inf")]
df_user = df_user[(df_user.AZ20_fold_change_log2 != "0")]

#calculating 3 scores
def mean_score(kinase, dataset):
    '''mean of the log2 FC of all phosphosites in the substrate set'''

    sub_set = dataset[dataset['KINASE'] == kinase]
    return print(sub_set['AZ20_fold_change_log2'].mean())

def alt_score(threshold, kinase, dataset):
    '''mean of the log2 FC for all SIGNIFICANT phosphosites in each substrate set'''
    sub_set = dataset[(dataset['KINASE'] == kinase) & (dataset['AZ20_p-value'] < threshold)]
    return print(sub_set['AZ20_fold_change_log2'].mean())

def delta_score(threshold, kinase, dataset):
    '''number of significant positive phosphosite minus
    significant down-regulated sites in each substrate set'''
    sub_set_neg = dataset[(dataset['KINASE'] == kinase) & (dataset['AZ20_p-value'] < threshold) &
                      (dataset['AZ20_fold_change_log2'] < 0)]
    sub_set_pos = dataset[(dataset['KINASE'] == kinase) & (dataset['AZ20_p-value'] < threshold) &
                          (dataset['AZ20_fold_change_log2'] > 0)]
    return print(len(sub_set_pos)-len(sub_set_neg))




mean_score("CDK1", df_user)
alt_score(0.05, "CDK1", df_user)
delta_score(0.05, "CDK1", df_user)



#volcano plot highlighting significant fold changes (plotly)

# x and y given as DataFrame columns

def volcano_plot(user_data):
    fig = px.scatter(df_user, x="AZ20_fold_change_log2", y="AZ20_p-value", color="AZ20_p-value",hover_data=["Substrate"])
    return fig.show()


volcano_plot(df_user)

#barplot showing kinase activity
import plotly.express as px


def kinase_barplot(user_data):
    sub_set = user_data[(user_data['KINASE'])]

    x_plot = []
    y_plot = []
    for x in sub_set:
        score1 = mean_score(x, user_data)
        x_plot.append(x)
        y_plot.append(score1)
    kinase_activity = pd.DataFrame(columns=(['x_plot'], ['y_plot']))
    fig = px.bar(kinase_activity, x=x_plot, y=y_plot)
    fig.show()

kinase_barplot(df_user)





