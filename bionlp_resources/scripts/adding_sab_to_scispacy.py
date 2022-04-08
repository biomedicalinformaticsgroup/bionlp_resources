import pickle
import pandas as pd
import numpy as np 

n = 0
path = 'full_text'

df_sab = pickle.load(open('./cui_to_sab.p', 'rb'))
df_abs = pickle.load(open(f'./{path}/spacy_umls_df{n}.p', 'rb'))

#df_abs = df_abs[['content_text', 'umls_ents', 'triggers', 'cuis', 'tuis', 'negation', 'spacy_ents']]

df_abs['sab'] = None

count = 0
for index, row in df_abs.iterrows():
    if (count % int(round(len(df_abs))/10) == 0 or count+1 == len(df_abs)) and count != 0: 
        print(str(f'The code for df{n} has completed: ') + str(round((count/len(df_abs))*100)) + str('%'))
    current_list = []
    if df_abs.loc[index].cuis == df_abs.loc[index].cuis:
        df_current = pd.DataFrame(df_abs.loc[index].cuis,
                            columns =['cui'])
        left_merged = pd.merge(df_current, df_sab,
                            how="left", on=["cui"])
        left_merged['sab'] = left_merged['sab'].apply(lambda d: d if isinstance(d, list) else [])
        current_list = list(left_merged.sab)
    df_abs.loc[index, 'sab'] = current_list
    count += 1

df_abs['hpo'] = None
df_abs['go'] = None
df_abs['rxnorm'] = None

for index, row in df_abs.iterrows():
    hpo_list= []
    go_list = []
    rxnorm_list = []
    for j in range(len(df_abs.loc[index].sab)):
        if 'GO' in df_abs.loc[index].sab[j]:
            go_list.append(True)
        else:
            go_list.append(False)
        if 'HPO' in df_abs.loc[index].sab[j]:
            hpo_list.append(True)
        else:
            hpo_list.append(False)
        if 'RXNORM' in df_abs.loc[index].sab[j]:
            rxnorm_list.append(True)
        else:
            rxnorm_list.append(False)
    df_abs.loc[index, 'hpo'] = hpo_list
    df_abs.loc[index, 'go'] = go_list
    df_abs.loc[index, 'rxnorm'] = rxnorm_list

pickle.dump(df_abs, open(f'./{path}/spacy_umls_df{n}.p', "wb"))
print(f'Process complete for {path} spacy_umls_df{n}')