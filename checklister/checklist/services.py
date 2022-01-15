from pprint import pprint

from django.shortcuts import redirect

from .models import Directory, CheckListTemplate


def get_directory(owner, directory_id):
    print('======get_directory======')
    directory_response = Directory.objects.filter(owner=owner, id=directory_id).values('id', 'name', 'parent')
    print(f'get_directory_response: {directory_response}')
    if directory_response:
        directory_response = directory_response[0]
        print('One string')
    print(f'get_directory_response_2: {directory_response}')
    return directory_response


def get_directory_list(owner, parent_directory_id=0):
    print('======get_directory_list======')
    directories = Directory.objects.filter(owner=owner, parent=parent_directory_id).values('id', 'name')
    print(f'Directories: {directories}')
    return directories


def get_parent_directory_path(owner, directory_id):
    print('======get_parent_directory_path======')
    parent_directory_path = '/'
    if directory_id == 0:
        return parent_directory_path
    flag = True
    while flag:
        directory = get_directory(owner=owner, directory_id=directory_id)
        pprint(f'directory = {directory}')
        if not directory:
            return redirect('/checklist/')
        elif directory['parent']:
            parent_directory_path = '/'+ directory['name'] + parent_directory_path
            directory_id = directory['parent']
        else:
            flag = False
    print(f'Parent directory path: {parent_directory_path}')
    return parent_directory_path


def get_directory_list_ajax(user, directory_id: int):
    print('======get_directory_list_ajax======')
    directory_list = get_directory_list(owner=user, parent_directory_id=directory_id)
    print(f'Directory list: {directory_list}')
    if directory_id == 0:
        parent_directory_path = '/'
    else:
        parent_directory_path = get_parent_directory_path(owner=user, directory_id=directory_id)
    response_list = [{'id': directory_id, 'name': parent_directory_path}]
    response_list.extend(directory_list)
    print(f'Response dictionary: {response_list}')
    response = dict(zip(range(len(response_list)), response_list))
    print(f'Response dictionary: {response}')
    return response


def add_new_directory(new_directory_name, parent_id, owner):
    new_directory = Directory(name=new_directory_name, parent=parent_id, owner=owner)
    print(new_directory.save())


def add_new_checklist(new_checklist_name, parent_id, owner):
    directory = Directory.objects.get(id=parent_id, owner=owner)
    print(f'Directory for creating checklist: {directory}')
    new_checklist = CheckListTemplate(name=new_checklist_name, directory=directory)
    print(f'New checklist object: {new_checklist}')
    print(new_checklist.save())
