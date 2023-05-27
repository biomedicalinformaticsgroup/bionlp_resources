# bionlp_resources
Repository where we can keep scripts related to other projects developed by the [biomedicalinformaticsgroup](https://github.com/biomedicalinformaticsgroup). This repository also has small bionlp project.

## Installation
bionlp_resources has dependencies on other Python packages, it is recommended to install it in an isolated environment

`git clone https://github.com/biomedicalinformaticsgroup/bionlp_resources.git`

`pip install ./bionlp_resources`

After installation, you can remove the file if you want using:

`rm -rf bionlp_resources`

You can also uninstall bionlp_resources using:

`pip uninstall bionlp_resources`

## Functions available in bionlp_resources

### Generating a DataFrame for HPO ID and CUI

This function is to create a DataFrame to map HPO identidifier to their corresponding CUI. HPO ID are generated from the [Human Phenotype Ontology](https://hpo.jax.org/app/). Using their OBO file available [here](https://hpo.jax.org/app/download/ontology).


```python
from bionlp_resources import cui_to_hpoid

cui_to_hpoid(
    path = './'
)
```
The function has only one parameter called 'path'. The default value is './' which means that the generated DataFrame will be saved in the current directory where the function is run in. Changing the default value allow to save the file to the given directory.

We are extracting 3 information saved in a pickle object called 'hpo_id_cui.p':

- hpo_id, it is starting by 'HP:'.
- hpo_value, it is the name associated to the HPO ID.
- cui, it is the coresponding UMLS CUI link to that hpo_id. One hpo_id can have multiple CUIs. Each one will be reporting on a different line. 

You can load the result using:

```python
import pickle
hpo_id_cui_df = pickle.load(open('{YOUR_PATH}/hpo_id_cui.p', 'rb'))
```

### Mapping the CUI to their corresponding [Source Abbreviation](https://www.nlm.nih.gov/research/umls/sourcereleasedocs/index.html)
This function is to link CUIs (Concept Unique Identifier) to their SAB (Source Abbreviation) from the UMLS (Unified Medical Language System). In order to use this function you will need to download the [MRCONSO.RRF](https://www.ncbi.nlm.nih.gov/books/NBK9685/table/ch03.T.concept_names_and_sources_file_mr/) file that you can find at [The National Library of Medicine website](https://www.nlm.nih.gov/research/umls/licensedcontent/umlsknowledgesources.html). 

```python
from bionlp_resources import cui_to_sab

cui_to_sab(
   path_to_rrf, 
   lang=None, 
   dest_path = './'
)
```
The function is taking 3 parameters: 
- path_to_rrf: the path to the MRCONSO.RRF file.
- lang: by default the function will load everything regardless of the language. If you want to focus on a specific language you can enter the language abbreviation like it is used in the MRCONSO.RRF file.
- dest_path: the default value is './' which means that 'cui_to_sab.p' will be saved in the current directory where the function is run. Changing the default value allow to save 'cui_to_sab.p' to the given directory.

We are extracting 2 information saved in a pickle object called 'cui_to_sab.p':
- CUI: Concept Unique Identifier from the UMLS.
- SAB: List of all the Source Abbreviation(s) listing a corresponding CUI in their ontology.

You can load the result using:

```python
import pickle
cui_to_sab_df = pickle.load(open('{YOUR_PATH}/cui_to_sab.p', 'rb'))
```

### PyGNormPlus

PyGNormPlus is a wrapper to call GNormPlus Java in Python using the subprocess library. GNormPlus is a tool developed by NIH and you can find out more on their website [GNormPlus: An Integrative Approach for Tagging Gene, Gene Family and Protein Domain](https://www.ncbi.nlm.nih.gov/research/bionlp/Tools/gnormplus/).

#### Requirements
First you will need to download and install the Java version of the tools available [here](https://www.ncbi.nlm.nih.gov/research/bionlp/Tools/gnormplus/). 

```python
from bionlp_resources import pygnormplus

pygnormplus(
    soft_dir_path, 
    input_dir_path, 
    output_dir_path = './'
)
```

The function is taking 3 parameters: 
- soft_dir_path: the directory to the GNormPlus jar file. It looks like ```$YOUR_PATH$/GNormPlusJava/GNormPlus.jar```.
- input_dir_path: the directory to the files you want to annotate. The only files that will be annotate are the ones with the .txt extension.
- output_dir_path: the default value is './' which means that the generated annotated files will be saved in the current directory where the function is run in within the 'output_gnormplus' file. Changing the default value allow to save the files to the given directory still in the 'output_gnormplus' file.

The result is a new directory called 'output_gnormplus' where the annotations are saved in text files using the same file name that from the original.

### PytmVar

PytmVar is a wrapper to call tmVar Java in Python using the subprocess library. tmVar is a tool developed by NIH and you can find out more on their website [tmVar: A text mining approach for extracting sequence variants in biomedical literature](https://www.ncbi.nlm.nih.gov/research/bionlp/Tools/tmvar/).

#### Requirements
First you will need to download and install the Java version of the tools available [here](https://www.ncbi.nlm.nih.gov/research/bionlp/Tools/tmvar/). 

```python
from bionlp_resources import pytmvar

pytmvar(
    soft_dir_path, 
    input_dir_path, 
    output_dir_path = './'
)
```

The function is taking 3 parameters: 
- soft_dir_path: the directory to the tmVar jar file. It looks like ```$YOUR_PATH$/tmVarJava/tmVar.jar```.
- input_dir_path: the directory to the files you want to annotate. The only files that will be annotate are the ones with the .txt extension.
- output_dir_path: the default value is './' which means that the generated annotated files will be saved in the current directory where the function is run in within the 'output_tmvar' file. Changing the default value allow to save the files to the given directory still in the 'output_tmvar' file.

The result is a new directory called 'output_tmvar' where the annotations are saved in text files using the same file name that from the original.

### Generating the DataFrame for TUIs to their corresponding semantic groups and types

This function is to create a DataFrame to map identifiers used in the UMLS with their [semantic types](https://lhncbc.nlm.nih.gov/ii/tools/MetaMap/Docs/SemanticTypes_2018AB.txt) and [semantic groups](https://lhncbc.nlm.nih.gov/ii/tools/MetaMap/Docs/SemGroups_2018.txt).


```python
from bionlp_resources import tuis_to_semantics

tuis_to_semantics(
    path = './'
)
```
The function has only one parameter called 'path'. The default value is './' which means that the generated DataFrame will be saved in the current directory where the function is run in. Changing the default value allow to save the file to the given directory.

We are extracting 5 information saved in a pickle object called 'tuis_to_semantics.p':

- abbreviation, the UMLS semantic type abbreviation.
- type_unique_identifier, the semantic type and group identifier.
- semantic_group_abbrev, the UMLS semantic group abbreviation.
- semantic_group_name, the UMLS semantic type name.
- full_semantic_type_name, the UMLS semantic group name.


You can load the result using:

```python
import pickle
tuis_to_semantics_df = pickle.load(open('{YOUR_PATH}/tuis_to_semantics.p', 'rb'))
```

## Biomedical NLP Data retrieval 

You can finb our GitHub automation to retrieve and parse PubMed abstract called [pm_abs_extr](https://github.com/biomedicalinformaticsgroup/pm_abs_extr).

You can finb our GitHub automation to retrieve and parse PubMed Central Open Access publications called [oa_pmc_extr](https://github.com/biomedicalinformaticsgroup/oa_pmc_extr).

You can find our GitHub automation to retrieve and parse full text publications from PubMed Query called [cadmus](https://github.com/biomedicalinformaticsgroup/cadmus).

## Biomedical Named Entity Recognition 

You can finb our GitHub project to use in parallel multiple MetaMap instances to annotate free text using the UMLS, more details can be find in our GitHub page [ParallelPyMetaMap](https://github.com/biomedicalinformaticsgroup/ParallelPyMetaMap).