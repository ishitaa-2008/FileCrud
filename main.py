#PROJECT ON CRUD OPERATIONSS

from pathlib import Path
import os
def readfileandfolder():
    p = Path('')
    items = list(p.rglob('*'))
    for index , file in enumerate(items):
        print(f'({index+1} - {file}')

 
def create_file():
    try:
        readfileandfolder()
        file_name = input('enter name of your file:')
        p = Path(file_name)
        if p.exists():
            print('FILE ALREADY EXIST')
        else:
            with open(file_name,'w') as file:
                content = input('enter ur content:')
                file.write(content)
                print('FILE ADDED!')
    except Exception as e:
        print("an error occured as{e}")



def read_file():
    try:
        readfileandfolder()
        file_name = input('enter name of your file')
        p = Path(file_name)
        if p.exists():
            with open(file_name,'r') as file:
                print(file.read())
            print("data readed successfully")
        else:
            print('FILE NOT FOUND')
    except Exception as e:
        print("an error occured as{e}")



def update_file():
    try:
        readfileandfolder()
        file_name = input('enter name of your file')
        p = Path(file_name)
        if p.exists():
            print('press 1 to overwrite the content')
            print('press 2 to append new content')

            option = int(input('enter your choice for updating a file'))
            if option == 1:
                with open(file_name,'w') as file:
                    content = input('enter your content')
                    file.write(content)
                    print('new content added')
            elif option == 2:
                with open(file_name,'a') as file:
                    content = input('enter your content')
                    file.write(""+content)
                    print('content added')
            else:
                print('Invalid Output')
        else:
            print('FILE DOES NOT EXISTS')
    except Exception as e:
        print("an error occured as{e}")



def delete_file():
    readfileandfolder()
    file_name = input('enter name of your file')
    p = Path(file_name)
    if p.exists():
        os.remove(p) #os is used for removing path of the file completely from the operating system
        print('File Deleted')
    else:
        print("File does not Exists")



def rename_file():
    readfileandfolder()
    file_name = input('enter name of your file')
    p = Path(file_name)
    if p.exists():
        new_file = input('enter new name of your file:')
        p.rename(new_file)
        print("FILE RENAMED")
    else:
        print('file not found')


def create_folder():
    readfileandfolder()
    folder_name = input('enter name of ypur folder:')
    p = Path(folder_name)
    if p.exists():
        print('folder already exists')
    else:
        p.mkdir()
        print('folder created!')





def delete_folder():
    readfileandfolder()
    folder_name = input('enter name of your folder:')
    p = Path(folder_name)
    if p.exists():
        p.rmdir()
        print('folder deleted!')
    else:
        print('file not found')


               

while True:
    print("press 1 for creating a file")
    print("press 2 for reading a file")
    print("press 3 for updating a file")
    print("press 4 for deleting a file")
    print("press 5 for renaming a file")
    print("press 6 for creating a folder")
    print("press 7 for deleting a folder")
    print("press 0 for exiting")


    option= int(input("enter your choice:"))
    if option == 1:
        create_file()
    if option == 2:
        read_file()
    if option == 3:
        update_file()
    if option == 4:
        delete_file()
    if option == 5:
        rename_file()
    if option == 6:
        create_folder()
    if option == 7:
        delete_folder()
    if option == 0:
        break



