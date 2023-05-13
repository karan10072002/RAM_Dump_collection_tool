import psutil
import sys
import os
import re
import random
import time
from tqdm import tqdm


def collect_process_ram_dump(process_name, output_file):
    for proc in psutil.process_iter(['pid', 'name']):
        if proc.info['name'] == process_name:
            pid = proc.info['pid']
            break
    else:
        print(f"Process '{process_name}' not found.")
        return
    os.system(f"rundll32.exe C:\\Windows\\System32\\comsvcs.dll, MiniDump {pid} {output_file} full")
    print(f"Memory dump file craetd for: [{process_name}] at [{output_file}] ")
    return

def collect_pagefile_info():
    pass

def collect_driver_info():
    pass

def collect_network_stat():
    pass

def get_all_process_id():
    new=os.popen('tasklist')
    all_pNames=[]
    all_pId=[]
    for i in new:
        try:
            if 'Image Name' not in i and '===============' not in i and i!=None:
                input_str = i
                # print(i)

                name_pattern = r"([A-Za-z.\s]+)"
                id_pattern = r"([0-9]+)"

                p_name = re.search(name_pattern, input_str)
                input_str = input_str.replace(str(p_name.group(0)), "")
                p_id = re.search(id_pattern, input_str)

                p_name = str(p_name.group(0)).strip(" ")
                p_id = str(p_id.group(0))

                all_pNames.append(p_name)
                all_pId.append(p_id)
        except:
            pass

    return all_pNames, all_pId

def progress_bar(progress, total):
    percent = 100 * (progress/float(total))
    bar = '█' * int(percent) + '-'*(100-int(percent))
    print(f"\r|{bar}| {percent:.2f}%", end="\r")

def removing_process_dumps(path, compiled_dump):
    for i in os.listdir():
        if i!= compiled_dump:
            os.remove(i)


#main

def main(meta_data = None):
    
    print("[ ] Getting all running processes...")
    all_process, all_pid = get_all_process_id()
    tasks = set(all_process)
    tasks = list(tasks)

    relative_path=os.getcwd()
    new_folder = os.path.join(relative_path, "All process dump collection")

    if "All process dump collection" not in os.listdir(relative_path):
        os.mkdir(new_folder)

    os.chdir(new_folder)


    print(f"saving info in {os.getcwd()}")
    for i in range(len(tasks)):
        collect_process_ram_dump(tasks[i], f"auto_gen_{i}.raw")

    print()
    print("[compiling...]")

    if meta_data:
        final_file_name=f"{meta_data['OS Name']}_{meta_data['System Type']} {meta_data['Host Name']}.raw"
    else:
        final_file_name = "complete RAM dump.raw"

    with open(final_file_name, "ab+") as gg:

        # no_of_processes = len(os.listdir())-1
        # counter=0

        for p_dumps in tqdm(os.listdir()):
            if p_dumps != final_file_name:
                with open(p_dumps, "rb") as ff:
                    gg.write(ff.read())
                    ff.close()
            # counter+=1

    print("[ ] RAM dump collection sucessful !")


if __name__ == '__main__':
    main()