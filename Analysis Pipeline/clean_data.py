import pandas as pd

df_sample = pd.read_table("sample_file.txt",
                          sep = "\t", delim_whitespace=True)
#delim_whitespace removes extra Nan columns
#df = df_sample.replace(np.nan, 0)
#optinal replace Nans with 0, not sure if necessary yet
#[15525 rows x 7 columns]
print(df_sample)

#correcting p values by Benjamini and Hochberg method

df_sample = df_sample.rename(columns = {'AZ20_p-value':'AZ20pvalues'})

def fdr(p_vals):

    from scipy.stats import rankdata
    ranked_p_values = rankdata(p_vals)
    fdr = p_vals * len(p_vals) / ranked_p_values
    fdr[fdr > 1] = 1

    return fdr

correct_pvals = fdr(df_sample.AZ20pvalues)

print(correct_pvals)
