import pickle
import numpy as np 
import pandas as pd
import requests

def cui_to_hpoid(path = './'):
    url = "https://raw.githubusercontent.com/obophenotype/human-phenotype-ontology/master/hp.obo"
    file = requests.get(url)
    content = str(file.text).split('\n')
    file.close()

    hpo_id = []
    hpo_name = []
    hpo_cui = []
    current_hpo = None
    current_name = None
    current_cui = []
    for i in range(len(content)):
        if 'xref: UMLS:' in content[i]:
            current_cui.append(content[i])
        if i == (len(content) -1):
            if current_cui != []:
                for j in range(len(current_cui)):
                    hpo_id.append(current_hpo)
                    hpo_name.append(current_name)
                    hpo_cui.append(current_cui[j])
        elif content[i+1] == '[Term]':
            if current_cui != []:
                for j in range(len(current_cui)):
                    hpo_id.append(current_hpo)
                    hpo_name.append(current_name)
                    hpo_cui.append(current_cui[j])
        if content[i] == '[Term]':
            current_hpo = content[i+1]
            current_name = content[i+2]
            current_cui = []

    for i in range(len(hpo_id)):
        hpo_id[i] = hpo_id[i].replace('id: ', '')

    for i in range(len(hpo_name)):
        hpo_name[i] = hpo_name[i].replace('name: ', '')

    for i in range(len(hpo_cui)):
        hpo_cui[i] = hpo_cui[i].replace('xref: UMLS:', '')

    df = pd.DataFrame(list(zip(hpo_id, hpo_name, hpo_cui)),
                columns =['hpo_id', 'hpo_value', 'cui'])

    pickle.dump(df, open(str(path + "hpo_id_cui.p"), "wb"))