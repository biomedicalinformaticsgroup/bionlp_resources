import requests
import pickle
import pandas as pd

url = "https://lhncbc.nlm.nih.gov/ii/tools/MetaMap/Docs/SemanticTypes_2018AB.txt"
file = requests.get(url)

semantictypes_sentences = str(file.text).split('\n')[:-1]

file.close()

abbreviation = []
type_unique_identifier = []
full_semantic_type_name = []

for i in range(len(semantictypes_sentences)):
    abbreviation.append(semantictypes_sentences[i].split('|')[0])
    type_unique_identifier.append(semantictypes_sentences[i].split('|')[1])

dict = {'abbreviation': abbreviation, 'type_unique_identifier': type_unique_identifier} 
df_semantictypes = pd.DataFrame(dict)

url = "https://lhncbc.nlm.nih.gov/ii/tools/MetaMap/Docs/SemGroups_2018.txt"
file = requests.get(url)

semgroups_sentences = str(file.text).split('\n')[:-1]

file.close()

semantic_group_abbrev = []
semantic_group_name = []
type_unique_identifier = []
full_semantic_type_name = []

for i in range(len(semgroups_sentences)):
    semantic_group_abbrev.append(semgroups_sentences[i].split('|')[0])
    semantic_group_name.append(semgroups_sentences[i].split('|')[1])
    type_unique_identifier.append(semgroups_sentences[i].split('|')[2])
    full_semantic_type_name.append(semgroups_sentences[i].split('|')[3])

dict = {'semantic_group_abbrev': semantic_group_abbrev, 'semantic_group_name' : semantic_group_name, 'type_unique_identifier': type_unique_identifier, 'full_semantic_type_name': full_semantic_type_name} 
df_semgroups = pd.DataFrame(dict)

tuis_to_semantics = df_semantictypes.merge(df_semgroups, on='type_unique_identifier', how='left')

pickle.dump(tuis_to_semantics, open("./tuis_to_semantics.p", "wb"))