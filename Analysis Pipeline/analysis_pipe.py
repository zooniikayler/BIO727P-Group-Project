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


df_user = df_user.rename(columns={[1]: 'newName1', 'oldName2': 'newName2'})

df_user['AZ20_fold_change_log2'] = np.log2(df_user['AZ20_fold_change'])


#adds the kinase names to the dataframe with user's data if their is a matching SUB_MOD_RSD and SUB_GENE
df_user = df_user.join(df_home[["KINASE_SYMBOL", "SUB_GENE", "SUB_MOD_RSD"]].set_index(["SUB_GENE", "SUB_MOD_RSD"]),
             on= ['Substrate', 'Position'])

df_home = df_user.join(df_home[["KINASE_SYMBOL", "SUB_ACC_ID", "SUB_MOD_RSD"]].set_index(["SUB_ACC_ID", "SUB_MOD_RSD"]),
             on= ['Substrate', 'Position'], rsuffix= '_sub_acc')

#cleaning data, removing Nans, O, infinity
df_user = df_user.dropna()
df_user= df_user.dropna(axis=0)
df_user = df_user.dropna(subset = ['KINASE_SYMBOL'])
df_user = df_user[(df_user.AZ20_fold_change_log2 != "inf")]
df_user = df_user[(df_user.AZ20_fold_change_log2 != "0")]

#calculating 3 scores
def mean_score(kinase, dataset):
    '''mean of the log2 FC of all phosphosites in the substrate set'''

    sub_set = dataset[dataset['KINASE_SYMBOL'] == kinase]
    return sub_set['AZ20_fold_change_log2'].mean()

def alt_score(threshold, kinase, dataset):
    '''mean of the log2 FC for all SIGNIFICANT phosphosites in each substrate set'''
    sub_set = dataset[(dataset['KINASE_SYMBOL'] == kinase) & (dataset['AZ20_p-value'] < threshold)]
    return print(sub_set['AZ20_fold_change_log2'].mean())

def delta_score(threshold, kinase, dataset):
    '''number of significant positive phosphosite minus
    significant down-regulated sites in each substrate set'''
    sub_set_neg = dataset[(dataset['KINASE_SYMBOL'] == kinase) & (dataset['AZ20_p-value'] < threshold) &
                      (dataset['AZ20_fold_change_log2'] < 0)]
    sub_set_pos = dataset[(dataset['KINASE_SYMBOL'] == kinase) & (dataset['AZ20_p-value'] < threshold) &
                          (dataset['AZ20_fold_change_log2'] > 0)]
    return len(sub_set_pos)-len(sub_set_neg)




#mean_score("CDK1", df_user)
#alt_score(0.05, "CDK1", df_user)
#delta_score(0.05, "CDK1", df_user)



#volcano plot highlighting significant fold changes (plotly)

# x and y given as DataFrame columns

def volcano_plot(user_data):
    fig = px.scatter(df_user, x="AZ20_fold_change_log2", y="AZ20_p-value", color="AZ20_p-value",hover_data=["Substrate"])
    return fig.show()


volcano_plot(df_user)

#barplot showing kinase activity
import plotly.express as px


#def kinase_barplot(user_data):
y_plot = set(df_user.KINASE_SYMBOL)
x_plot = []

for k in y_plot:
    x = mean_score(k, df_user)
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





