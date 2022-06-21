# bionlp_resources
Repository where we can keep scripts related to other projects developed by the [biomedicalinformaticsgroup](https://github.com/biomedicalinformaticsgroup/ParallelPyMetaMap). This repository also has small bionlp project.

## Installation
bionlp_resources has dependencies on other Python packages, it is recommended to install it in an isolated environment

`git clone https://github.com/biomedicalinformaticsgroup/bionlp_resources.git`

`pip install ./bionlp_resources`

After installation, you can remove the file if you want using:

`rm -rf bionlp_resources`

You can also uninstall bionlp_resources using:

`pip uninstall bionlp_resources`

## Functions available in bionlp_resources

### Generating the table for HPO ID and CUI

```python
from bionlp_resources import cui_to_hpoid

cui_to_hpoid(
    path = './'
)
```

This function is to create a table to map HPO identidifier to their corresponding CUI. HPO ID are generated from the [Human Phenotype Ontology](https://hpo.jax.org/app/). Using their OBO file available [here](https://hpo.jax.org/app/download/ontology) we are extracting 3 information saved in a pickle object called 'hpo_id_cui.p':

- hpo_id, it is starting by 'HP:'.
- hpo_value, it is the name associated to the HPO ID.
- cui, it is the coresponding UMLS CUI link to that hpo_id. One hpo_id can have multiple CUIs. Each one will be reporting on a different line. 

The function has only one parameter called 'path'. The default value is './' which means that the generated table will be saved on the current directory where the function is run in. Changing the default value is saving the file to the given directory.

```python
import pickle
hpo_id_cui_df = pickle.load(open('{YOUR_PATH}/hpo_id_cui.p', 'rb'))
```

### Mapping the CUI to their corresponding [Source Abbreviation](https://www.nlm.nih.gov/research/umls/sourcereleasedocs/index.html)



### Pubmed Central Open Access Corpus Generation 

```python
from bionlp_resources import pmc_oa_generation

pmc_oa_generation(
    path = './'
)
```

This script is to generate a DataFrame saved as a pickle object as well as a directory that contains all the open access publications indexed in [PubMed Central](https://www.ncbi.nlm.nih.gov/pmc/). The function is collecting the publications using the ftp page available [here](https://ftp.ncbi.nlm.nih.gov/pub/pmc/).

The funtion has only one optional parameter called 'path'. This parameter is to identify where to save the result. The default value is './' also known as the current directory. 

Once the function is called it will create a directory '{YOUR_PATH}/pmc_oabulk_output_{TODAY_DATE}'. Inside this directory you will find:
- /zip_files, it contains all the tgz files from the ftp request. 
- /unzip_files, it contain all the extracted files from the ftp request. 
- /pmcid_subdirect.txt, this txt file references all the subdirectories and files present in the unzip_files directory. For example, you can find the path to a specific PMCID (PubMed Central Identifier).
- /PMC_oa_full_text.p, this pickle object is a Pandas DataFrame with 4 columns:
  - pmcid (PubMed Central Identifier)
  - path, it is the relative path to the file from the output. 
  - unparsed_text, the content from the PMCID txt file we got from the ftp request without parsing or operation to change its content.
  - parsed_text,  the content from the PMCID txt file we got from the ftp request that is present between the 'Body' and 'Refs'. We also remove the unicode and tags. 

```python
import pickle
pmc_oa_df = pickle.load(open('{YOUR_PATH}/pmc_oabulk_output_{TODAY_DATE}/PMC_oa_full_text.p', 'rb'))
```

### PyGNormPlus

```python
from bionlp_resources import pygnormplus

pygnormplus(
    soft_dir_path, 
    input_dir_path, 
    output_dir_path = './'
)
```

PyGNormPlus is a wrapper to call GNormPlus Java in Python using the subprocess library. GNormPlus is a tool developed by NIH and you can find out more on their website [GNormPlus: An Integrative Approach for Tagging Gene, Gene Family and Protein Domain](https://www.ncbi.nlm.nih.gov/research/bionlp/Tools/gnormplus/).

#### Requirements
First you will need to download and install the Java version of the tools available [here](https://www.ncbi.nlm.nih.gov/research/bionlp/Tools/gnormplus/). 


### PytmVar

### Generating the table for TUIs to semantics group and type