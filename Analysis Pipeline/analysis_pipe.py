import pandas as pd
import numpy as np
import plotly.express as px
import sqlite3

#connecting to the database
conn = sqlite3.connect("KinaseDatabasev1.db")
SQL_Query = pd.read_sql_query("SELECT Substrate.Kinase, Substrate.Substrate_Symbol,Substrate.Sub_Gene, Substrate.Sub_Mod_Rsd FROM Substrate",conn)

#import data as dataFrame
df_user = pd.read_table("sample_file.txt")
df_home = pd.DataFrame(SQL_Query, columns=['Kinase','Substrate_Symbol','Sub_Gene','Sub_Mod_Rsd'])

#preparing uploaded data
#requires CSV uploaded with columns [1] Substrates(Position) [2] control_mean [3] condition_mean [4] FC [5] p_val [6] Any
#def prepare_user_data(df_user, df_home):
df_user['Position'] = ''
df_user['Position'] = df_user.Substrate.str.split("(", n=1, expand = True)[1].str.replace(")", "")
df_user['Substrate'] = df_user.Substrate.str.split("(", n=1, expand = True)[0]
#print(list(df_user.columns.values))
df_user.columns = ('Substrate', 'control_mean2', 'condition_mean3', 'FC4', 'pval5', 'cv_control6', 'cv_condition7', 'Position')
#print(list(df_user.columns.values))
df_user['FC_log2'] = np.log2(df_user['FC4'])

#adds the kinase names to the dataframe with user's data if their is a matching SUB_MOD_RSD and SUB_GENE
df_user = df_user.join(df_home[["Kinase", "Sub_Gene", "Sub_Mod_Rsd"]].set_index(["Sub_Gene", "Sub_Mod_Rsd"]),
                 on= ['Substrate', 'Position'])

df_home = df_user.join(df_home[["Kinase", "Substrate_Symbol", "Sub_Mod_Rsd"]].set_index(["Substrate_Symbol", "Sub_Mod_Rsd"]),
                 on= ['Substrate', 'Position'], rsuffix= '_sub_acc')

#cleaning data, removing Nans, O, infinity
df_user = df_user.dropna()
df_user= df_user.dropna(axis=0)
df_user = df_user.dropna(subset = ['Kinase'])
df_user = df_user[(df_user.FC_log2 != "inf")]
df_user = df_user[(df_user.FC_log2 != "0")]


#calculating 3 scores
def mean_score(kinase, dataset):
    '''mean of the log2 FC of all phosphosites in the substrate set'''

    sub_set = dataset[dataset['Kinase'] == kinase]
    return sub_set['FC_log2'].mean()

def alt_score(threshold, kinase, dataset):
    '''mean of the log2 FC for all SIGNIFICANT phosphosites in each substrate set'''
    sub_set = dataset[(dataset['Kinase'] == kinase) & (dataset['pval5'] < threshold)]
    return print(sub_set['FC_log2'].mean())

def delta_score(threshold, kinase, dataset):
    '''number of significant positive phosphosite minus
    significant down-regulated sites in each substrate set'''
    sub_set_neg = dataset[(dataset['Kinase'] == kinase) & (dataset['pval5'] < threshold) &
                      (dataset['FC_log2'] < 0)]
    sub_set_pos = dataset[(dataset['Kinase'] == kinase) & (dataset['pval5'] < threshold) &
                          (dataset['FC_log2'] > 0)]
    return len(sub_set_pos)-len(sub_set_neg)


#volcano plot highlighting significant fold changes (plotly), x and y given as DataFrame columns
def volcano_plot(user_data):
    fig = px.scatter(user_data, x="FC_log2", y="pval5", color="pval5",hover_data=["Substrate"])
    return fig.show()
#barplot showing kinase activity
def kinase_barplot(user_data):
    y_plot = set(user_data.KINASE_SYMBOL)
    x_plot = []

    for k in y_plot:
        x = mean_score(k, user_data)
        x_plot.append(x)

    labels = ['Activity','Kinase']
    kin_activity = pd.DataFrame(columns=labels)
    kin_activity['Activity']=x_plot
    kin_activity['Kinase']=y_plot
    kin_activity.sort_values(['Activity'], ascending=[True])

    fig = px.bar(kin_activity, color='Activity',  y='Activity', x='Kinase')
    fig.update_layout(
        title='Relative Kinase Activity' + " User Uploaded Data",
        xaxis_tickfont_size=14,
        yaxis=dict(
            title='Activity',
            titlefont_size=16,
            tickfont_size=14))
    fig.update_layout(xaxis={'categoryorder':'total ascending'})
    fig.show()
    return

#prepare_user_data(df_user1, df_home1) #returns df_user1
kinase_barplot(df_user)



