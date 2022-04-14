import subprocess
import os
import shutil
import multiprocessing as mp

def annotation_func_tmVar(my_list, soft_dir_path, pwd, input_dir_path, output_dir_path):
    for i in range(len(my_list)):
        if len(my_list) > 9:
            if (i % int(round(len(my_list))/10) == 0 or (i+1 == len(my_list)) and i-1 % int(round(len(my_list))/10) != 0) and i != 0: 
                print(str(f'We have annotated: ') + str(round((i/len(my_list))*100)) + str('%' +  ' of the input directory.'))
        else:
            print(str(f'We have annotated file number : ') + str(i) + str('out of ') + str(len(my_list)))
        f = open(f"{input_dir_path}/{my_list[i]}", "r")
        my_str = f.readline()
        try:
            os.mkdir(f'./temp_input')
            os.mkdir(f'./temp_output')
        except:
            pass
        f = open(f"./temp_input/{my_list[i]}", "w")
        f.write(f"{my_list[i].split('.')[0]}|t|{my_str}\n\n")
        f.close()
        subprocess.check_call(['java', '-Xmx5G', '-Xms5G', '-jar', soft_dir_path.split('/')[-1], pwd+f'/temp_input', pwd+'/temp_output'], cwd='/'.join(soft_dir_path.split('/')[:-1]))
        current_doc = []
        f = open(f"./temp_output/{my_list[i]}.PubTator", "r")
        for x in f:
            current_doc.append(x)
        current_doc = current_doc[1:]
        f.close()
        total_doc = []
        current_line = []
        for j in range(len(current_doc)):
            if len(current_doc[j].split('\t')) > 1:
                current_line = []
                current_line.append(current_doc[j].split('\t')[0])
                current_line.append(current_doc[j].split('\t')[1])
                current_line.append(current_doc[j].split('\t')[2])
                current_line.append(current_doc[j].split('\t')[3])
                current_line.append(current_doc[j].split('\t')[4])
                total_doc.append(current_line)
        for k in range(len(total_doc)):
            f = open(f"{output_dir_path}/output_tmVar/{my_list[i]}", "a")
            f.write(str(total_doc[k]))
            if k < len(total_doc)-1:
                f.write('\n')
        if len(total_doc) == 0:
            f = open(f"{output_dir_path}/output_tmVar/{my_list[i]}", "a")
            f.write(str([]))

def pygnormplus(soft_dir_path, input_dir_path, output_dir_path = './'):
    pwd = os.getcwd()
    try:
        os.mkdir(f'{output_dir_path}/output_tmVar')
        list_done = []
    except:
        list_done = subprocess.getstatusoutput(f"ls -lR {output_dir_path}/output_tmVar")
        list_done = list(list_done)
        list_done = list_done[1]
        list_done = str(list_done).split('\n')
        my_list = []
        for i in range(len(list_done)):
            my_list.append(list_done[i])
        list_done = my_list
    try:
        shutil.rmtree('./temp_input')
    except:
        pass
    try:
        shutil.rmtree('./temp_output')
    except:
        pass

    command = subprocess.getstatusoutput(f"ls -lR {input_dir_path}")
    command = list(command)
    command = command[1]
    command = str(command).split('\n')
    my_list = []
    for i in range(len(command)):
        my_list.append(command[i])
    
    if list_done != []:
        my_list = list(set(my_list) - set(list_done))

    annotation_func_tmVar(my_list, soft_dir_path, pwd, input_dir_path, output_dir_path)

    print('Process completed')