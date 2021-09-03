#!/usr/bin/env python
import os
import magic
# import collections
import shutil
from time import sleep
from os import system,name
from time import sleep
from colorama import Fore, Style
from rich.table import Table
from rich.console import Console

os.system("title Folder Organizer By YanPaingOo")
os.system('cls' if os.name == 'nt' else 'clear')

console = Console()

dest_dir = "/Users/sherrinford/Documents/"
source_dir = "/Users/sherrinford/Downloads/"
file_type_and_name = {"Directory": []}

def mode_selection():
    selection_list = ['a','m','A','M']
    user_selection = userinput(selection_list)
    print(user_selection)
    if user_selection == "a" or user_selection == "A":
        print("Auto Mode Selected")
    else:
        print("Manual Selected")

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
        tasks =  [f"Creating Folder {input_type}"]

        with console.status("[bold green]Creating Folder") as status:
            while tasks:
                task = tasks.pop(0)
                sleep(1)
                console.log(f"{task} Complete")

        os.mkdir(dest_dir + input_type)
        return dest_dir + input_type

def file_type_check(input_type):

    if input_type not in file_type_and_name:
        print("Your selected type is not available")

def move_func(source_dir,move_dir,item_list):

    for item in item_list:
        item_source_path = source_dir + item
        item_dest_path = str(move_dir)+ "/" + item
        shutil.move(item_source_path,item_dest_path)

    tasks = [f"Moving {item}" for item in item_list]

    with console.status("[bold white]Moving ... ",spinner='aesthetic') as status:
        while tasks:
            task = tasks.pop(0)
            sleep(1)
            console.log(f"{task} Complete")

def screen_clean():
    if name == 'nt':
        _ = system('cls')
    else:
        _ = system('clear')

def userinput(list_for_input):

    input_type = input("Enter your choice : ")

    while input_type not in list_for_input:
        print("Invalid input {}".format(input_type))
        input_type = input("Enter your choice : ")
    return input_type

def input_type_check(input_type):
    if input_type == "all":
        for key,values in file_type_and_name.items():
            move_dir = folder_exits_check(dest_dir,key)
            move_func(source_dir,move_dir,values)



show_file_and_directory(source_dir)
print("Eg: image  or For all Enter All")

# file_list,file_type = userinput()
# print(file_list)
# print(file_type)
# move_dir = folder_exits_check(dest_dir,file_type)

# move_func(source_dir,dir,file_list)

mode_selection()
