import os
import magic
import collections
import shutil
from time import sleep
from colorama import Fore, Style
from rich.table import Table
from rich.console import Console

dest_dir = "/Users/sherrinford/Documents/"
source_dir = "/Users/sherrinford/Downloads/"
file_type_and_name = collections.defaultdict(list)
file_type_and_name = { "application": [] ,"Directory": [],"video":[]}

def show_file_and_directory(source_dir):

    all_files = os.listdir(source_dir)
    count = 1
    data = []

    for file in all_files:
        if not file.startswith('.'):
            if os.path.isfile(source_dir + file):
                data.append([count,file,magic.from_file(source_dir+file,mime=True)])
                file_type = str(magic.from_file(source_dir + file,mime=True)).rsplit('/',1)[0]
                store_data(file_type,file)
                count += 1
            else:
                data.append([count,file,"Directory"])
                file_type_and_name["Directory"].append(str(file))
                count +=1

    show_as_table(data)

def store_data(file_type,file_name):
    if file_type not in file_type_and_name:
        file_type_and_name[file_type] = []
        file_type_and_name[file_type].append(file_name)
    else:
        file_type_and_name[file_type].append(file_name)

def show_as_table(data):
    console = Console()
    table = Table(title="All Files and Directory in Downloads",show_header=True,header_style="bold green")
    t_header = ['No', 'File Name', 'Type']
    for num in t_header:
        table.add_column(num)

    for d in data:
        table.add_row(str(d[0]),str(d[1]),str(d[2]).rsplit('/',1)[0])
    console.print(table)

def folder_exits_check(dest_dir,input_type):
    input_type = input_type.capitalize()

    if os.path.isdir(dest_dir + input_type):
        print("{} DIR EXIST {}{}".format(Fore.GREEN,input_type,Style.RESET_ALL ) )
        return dest_dir + input_type
    else:
        print("{} NOT EXIST: {}{}".format(Fore.RED,input_type,Style.RESET_ALL))



show_file_and_directory(source_dir)
print("Eg: image  or For all Enter All")
input_type = input("Choose File Type: ")
mov_list = file_type_and_name[input_type]

dir = folder_exits_check(dest_dir,input_type)

def move_func(source_dir,dir,item_list):
    console = Console()

    # for item in item_list:
        # item_source_path = source_dir + item
        # item_dest_path = str(dir)+ "/" + item
        # shutil.move(item_source_path,item_dest_path)

    tasks = [f"Moving {item}" for item in item_list]

    with console.status("[bold white]Moving ... ",spinner='aesthetic') as status:
        while tasks:
            task = tasks.pop(0)
            sleep(1)
            console.log(f"{task} Complete")

move_func(source_dir,dir,mov_list)
