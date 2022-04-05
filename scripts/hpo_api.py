import pickle
import json 
df = pickle.load(open('hpo_id_cui.p', 'rb'))
diseases_list_dict = []
genes_list_dict = []
for i in range(len(df)):
    try:
        response = json.loads(open(f'./jsons/{df.iloc[i].hpo_id}.json').read())
        diseases_list_dict.append(response.get('diseases'))
        genes_list_dict.append(response.get('genes'))
    except:
        diseases_list_dict.append(['No API file'])
        genes_list_dict.append(['No API file'])

        
df['hpo_diseases_dict'] = diseases_list_dict
df['hpo_genes_dict'] = genes_list_dict
diseases_list = []
genes_list = []
for i in range(len(df)):
    current_diseases = []
    current_genes = []
    for j in range(len(df.iloc[i].hpo_diseases_dict)):
        current_diseases.append(df.iloc[i].hpo_diseases_dict[j].get('dbName'))
    for j in range(len(df.iloc[i].hpo_genes_dict)):
        current_genes.append(df.iloc[i].hpo_genes_dict[j].get('entrezGeneSymbol'))
    diseases_list.append(current_diseases)
    genes_list.append(current_genes)


df['hpo_diseases'] = diseases_list
df['hpo_genes'] = genes_list
pickle.dump(df, open(f'./hpo_api.p', 'wb'))