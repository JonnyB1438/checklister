from pprint import pprint

from django.shortcuts import redirect

from .models import Directory, CheckListTemplate


def get_directory(owner, directory_id):
    print('======get_directory======')
    directory_response = Directory.objects.filter(owner=owner, id=directory_id).values('id', 'name', 'parent')
    if directory_response:
        directory_response = directory_response[0]
    print(f'get_directory_response: {directory_response}')
    return directory_response


def get_directories_by_parent(owner, parent_id):
    return Directory.objects.filter(owner=owner, parent=parent_id).values('id', 'name')


def get_directory_checklists(owner, directory_id):
    directory = Directory.objects.get(id=directory_id, owner=owner)
    return CheckListTemplate.objects.filter(directory=directory).values('id', 'name')


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
            return redirect('checklist')
        elif directory['parent']:
            parent_directory_path = '/'+ directory['name'] + parent_directory_path
            directory_id = directory['parent']
        else:
            flag = False
    print(f'Parent directory path: {parent_directory_path}')
    return parent_directory_path


def get_directory_list_ajax(user, directory_id: int):
    print('======get_directory_list_ajax======')
    # directory_list = get_directory_list(owner=user, parent_directory_id=directory_id)
    directory_list = get_directories_by_parent(owner=user, parent_id=directory_id)
    print(f'Directory list: {directory_list}')
    if directory_id == 0:
        parent_directory_path = '/'
    else:
        parent_directory_path = get_parent_directory_path(owner=user, directory_id=directory_id)
    directory_checklists = get_directory_checklists(owner=user, directory_id=directory_id)
    directory_response_list = [{'id': directory_id, 'name': parent_directory_path}]
    directory_response_list.extend(directory_list)
    print(f'Response dictionary: {directory_response_list}')
    directory_response_dict = dict(zip(range(len(directory_response_list)), directory_response_list))
    checklist_response_dict = dict(zip(range(len(directory_checklists)), directory_checklists))
    response = {'directories': directory_response_dict, 'checklists': checklist_response_dict}
    print(f'Response dictionary: {response}')
    return response


def add_new_directory(new_directory_name, parent_id, owner):
    new_directory = Directory(name=new_directory_name, parent=parent_id, owner=owner)
    print(new_directory.save())
    return {'id': new_directory.pk, 'name': new_directory.name}


def add_new_checklist(new_checklist_name, parent_id, owner):
    directory = Directory.objects.get(id=parent_id, owner=owner)
    print(f'Directory for creating checklist: {directory}')
    new_checklist = CheckListTemplate(name=new_checklist_name, directory=directory)
    print(f'New checklist object: {new_checklist}')
    print(new_checklist.save())


def is_checklist(id, directory):
    return CheckListTemplate.objects.filter(id=id, directory=Directory.objects.get(id=directory))


def delete_checklist(id):
    CheckListTemplate.objects.filter(id=id).delete()


def delete_directory(id):
    print(f'========Start function for id={id}')
    child_directories = Directory.objects.filter(parent=id).values('id')
    print(f'Child directories: {child_directories}')
    if child_directories:
        for child_directory in child_directories:
            delete_directory(child_directory['id'])
    print(f'Deletion directory id=: {id}')
    Directory.objects.filter(id=id).delete()
