import pickle
import pandas as pd 
import numpy as np
import wget
from bs4 import BeautifulSoup
import os
from datetime import date
import time
import tarfile
import subprocess
import re
import unicodedata

fdate = date.today().strftime('%d%m%Y')
path = f"./pmc_oabulk_output_{fdate}"

try:
    os.mkdir(path)
    os.mkdir(f"./pmc_oabulk_output_{fdate}/unzip_files")
    os.mkdir(f"./pmc_oabulk_output_{fdate}/zip_files")
except:
    pass

url = [
        'https://ftp.ncbi.nlm.nih.gov/pub/pmc/oa_bulk/oa_noncomm/txt/',
        'https://ftp.ncbi.nlm.nih.gov/pub/pmc/oa_bulk/oa_comm/txt/'
        ]

for j in range(len(url)):
    filename = wget.download(url[j], out=f'./{path}')
    print('\n')
    print(f'Retrieving link: {url[j]}')
    soup = BeautifulSoup(open(f'./{path}/download.wget'))
    links = soup.find_all('a')
    links = links[1:]
    base_url = url[j]
    complete_links = []
    for i in range(len(links)):
        complete_links.append(str(base_url) + str(links[i].attrs['href']))

    for i in range(len(complete_links)):
        if complete_links[i] == 'https://ftp.ncbi.nlm.nih.gov/pub/pmc/oa_bulk/oa_noncomm/':
            pass
        elif complete_links[i] == 'https://www.hhs.gov/vulnerability-disclosure-policy/index.html':
            pass
        else:
            try:
                filename = wget.download(complete_links[i], out=f"./pmc_oabulk_output_{fdate}/zip_files")
                print('\n')
                print(f'Retrieving link: {complete_links[i]}')
                time.sleep(1)
            except:
                time.sleep(1)
    os.remove(f'./{path}/download.wget')

print('Retrieval process completed')

for file in os.listdir(f"./pmc_oabulk_output_{fdate}/zip_files"):   # get the list of files
    if '.tar.gz' in str(file): # if it is a zipfile, extract it
        # open file
        unzip_file = tarfile.open(str(f"./pmc_oabulk_output_{fdate}/zip_files/") + str(file))
        # extracting file
        unzip_file.extractall(f"./pmc_oabulk_output_{fdate}/unzip_files")
        unzip_file.close()

print('Unzip process completed')

command = subprocess.getstatusoutput(f"ls -lR ./pmc_oabulk_output_{fdate}/unzip_files")
command = list(command)
command = command[1]
command = str(command).split('\n')
my_list = []
for i in range(len(command)):
    my_list.append(command[i])
command = my_list

for i in range(len(command)):
    f = open(f"./pmc_oabulk_output_{fdate}/pmcid_subdirect.txt", "a")
    f.write(str(command[i]))
    f.close()

files = []
current_string = str
for i in range(len(command)):
    if './pmc' in command[i]:
        current_string = command[i][:-1]
    if len(command[i].split()) > 1:
        if 'PMC' in command[i].split()[-1][:3] and '.txt' in command[i].split()[-1][-5:]:
            files.append(str(current_string) + str('/') + str(command[i].split()[-1]))

pmc_files = []
pmc_name = []
for i in range(len(files)):
    matches = re.findall('/PMC.+?.txt',files[i][-15:])
    if matches != []:
        pmc_files.append(files[i])
        pmc_name.append(matches[0][1:-4])

df_path = pd.DataFrame(
                    {'pmcid': pmc_name,
                    'path': pmc_files
                    })

text = []
for i in range(len(df_path)):
    if i % 100000 == 0 and i != 0:
        print(str('We have passed unparsed text ') + str(i) + str('out of ') + str(len(df_path)))
    try:
        f = open(df_path.iloc[i].path, "r")
        text.append(f.read().encode('utf-8', 'ignore').decode())
    except:
        text.append('')
print('Unparsed text completed')

df_path['unparsed_text'] = text
text = []

parse_text = []
for i in range(len(df_path)):
    if i % 100000 == 0 and i != 0:
        print(str('We have passed parsed text ') + str(i) + str('out of ') + str(len(df_path)))
    curent_list = []
    if df_path.iloc[i].unparsed_text != '':
        curent_list = df_path.iloc[i].unparsed_text.split('\n')
        lower = 0
        upper = len(curent_list)
        for j in range(len(curent_list)):
            if curent_list[j] == '==== Body':
                lower = j+1
            if curent_list[j] == '==== Refs':
                upper = j-1
        curent_text = str(' '.join(curent_list[lower:upper]))
        curent_text = unicodedata.normalize("NFKD", curent_text)
        curent_text = curent_text.replace('\t', ' ')
        try:
            curent_text = curent_text.replace('\\u', ' ')
        except:
            pass
        parse_text.append(curent_text)
    else:
        parse_text.append('')
print('Parsed text completed')

df_path['parsed_text'] = parse_text

pickle.dump( df_path, open( f"./pmc_oabulk_output_{fdate}/PMC_oa_full_text.p", "wb" ) )
print('Process completed')