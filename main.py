#!/usr/bin/env python
import os
import magic
import shutil
from time import sleep
from os import system,name
from time import sleep
from colorama import Fore, Style
from rich.table import Table
from rich.console import Console


os.system('cls' if os.name == 'nt' else 'clear')

console = Console()

home_dir    =   os.path.expanduser('~')
dest_dir = home_dir + "/Documents/"
source_dir = home_dir + "/Downloads/"
file_type_and_name = {"Directory": []}


def mode_selection():
    selection_list = ["1","2"]
    console.print("1.Auto Mode", style="bold green")
    console.print("2.Manual Mode", style="bold red")
    user_selection = userinput(selection_list)
    print(user_selection)
    if user_selection == "1":
        console.print("Auto Mode Selected", style="bold green")
        auto_mode()
    else:
        console.print("Manual Selected", style="bold red")
        manual_mode()


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

    return data


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
        table.add_row(
            "[dim]" + str(d[0])+ "[/dim]",
            str(d[1]),
            "[bold]" + str(d[2]).rsplit('/',1)[0] + "[/bold]"
            )
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


def auto_mode():
    result = show_file_and_directory(source_dir)
    if result:
        screen_clean()
        show_as_table(result)
        for key,values in file_type_and_name.items():
            move_dir = folder_exits_check(dest_dir,key)
            move_func(source_dir,move_dir,values)
    else:
        print("There is no files or folder in "+source_dir)


def manual_mode():
    result =   show_file_and_directory(source_dir)
    if result:
        screen_clean()
        show_as_table(result)
        console.print("[dim]Eg: image [/dim]")
        file_type_list = file_type_and_name.keys()
        user_selection  = userinput(file_type_list)

        move_dir = folder_exits_check(dest_dir,user_selection)
        file_list = get_file_list(user_selection)
        move_func(source_dir,move_dir,file_list)
    else:
        print("There is no files or folder in "+source_dir)


def get_file_list(file_type):
    file_list = None
    for key,values in file_type_and_name.items():
        if key == file_type:
            file_list = values
    return file_list


def main():
    mode_selection()


if __name__ == "__main__":
    main()
