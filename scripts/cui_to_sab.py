import pickle
import pandas as pd 
import numpy as np

def cui_to_sab(path, lang=None):
    master_sources = pd.read_csv(path, delimiter='|', usecols=[0,1,11], names=['cui', 'lang', 'sab'])

    if lang != None:
        master_sources = master_sources[master_sources.lang == lang]
        master_sources = master_sources.drop("lang", axis=1)        
    else:
        pass

    master_sources = master_sources.drop_duplicates()
    master_sources = master_sources.reset_index(drop=True)
    aggregation_functions = {'sab': lambda x: list(x)}
    master_sources = master_sources.groupby(['cui']).aggregate(aggregation_functions)
    master_sources = master_sources.reset_index()

    pickle.dump(master_sources, open("./cui_to_sab.p", "wb"))