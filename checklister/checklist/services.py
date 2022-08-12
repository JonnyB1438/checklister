# import urllib.request

import django.contrib.auth.models
from django.http.response import JsonResponse
from requests import Request

from .models import Directory, CheckListTemplate

User = django.contrib.auth.models.User


def get_directory(owner: User, directory_id: int) -> dict:
    """
    Performs a secure existence check of a directory by an owner (using filter method).

    :param owner: a user of an auth user type.
    :param directory_id: a checking directory id.
    :return: An empty dictionary or a dictionary with keys 'id', 'name' and 'parent' of founded directory.
    """
    directory_response = Directory.objects.filter(owner=owner, id=directory_id).values('id', 'name', 'parent')
    directory_response = directory_response[0] if directory_response else {}
    return directory_response


def get_root_directory(owner: User) -> dict:
    """
    Check an auth user root directory, if it does not exist, create it.
    Return a dict with keys: 'id', 'name' of the root directory.

    :param owner: a user of an auth user type.
    :return: a dict with keys: 'id', 'name' of the root directory.
    """
    root_directory = Directory.objects.filter(owner=owner, parent__isnull=True).values('id', 'name')
    if not root_directory:
        root_directory = add_new_directory(new_directory_name='/', parent_directory_id=None, owner=owner)
    else:
        root_directory = root_directory[0]
    return root_directory


def get_checklists_by_directory(owner: User, directory_id: int) -> list[Directory]:
    """
    Return a list of checklists in an owner directory as dictionaries with keys: 'id', 'name'.

    :param owner: a user of an auth user type.
    :param directory_id: a search directory id.
    :return: a list of dictionaries with keys: 'id', 'name'.
    """
    directory = Directory.objects.get(id=directory_id, owner=owner)
    return CheckListTemplate.objects.filter(directory=directory).values('id', 'name')


def update_directory_data(owner: User, directory_id: int, directory_name=None, parent_directory_id=None) -> bool:
    """
    Change a directory(name, parent) with checking of an owner(directory and parent).

    :param owner: a user of an auth user type.
    :param directory_id: a changing directory ID.
    :param parent_directory_id: a new parent directory ID.
    :param directory_name: a new directory name.
    :return: True if everything is OK, else - False
    """
    directory = Directory.objects.get(id=directory_id, owner=owner)
    if directory_name:
        directory.name = directory_name
        directory.save()
    if parent_directory_id:
        if Directory.objects.get(id=parent_directory_id, owner=owner):
            directory.parent = Directory.objects.get(id=parent_directory_id)
            directory.save()
        else:
            return False
    return True


def move_directory_up_from_current_directory(owner: User, directory_id: int, current_directory_id: int) -> bool:
    """
    Move a directory up from a current directory with checking of their owner.

    :param owner: a user of an auth user type.
    :param directory_id: a moving directory ID.
    :param current_directory_id: a current directory ID.
    :return: True if everything is OK, else - False
    """
    target_directory_id = Directory.objects.get(id=current_directory_id, owner=owner).parent.id
    if update_directory_data(owner=owner, directory_id=directory_id, parent_directory_id=target_directory_id):
        return True
    return False


def move_checklist_into_directory(owner: User, checklist_id: int, target_directory_id: int) -> bool:
    """
    Move a checklist to another directory with checking of their owner.

    :param owner: a user of an auth user type.
    :param checklist_id: a moving checklist ID.
    :param target_directory_id: a target directory ID.
    :return: True if everything is OK, else - False
    """
    checklist = CheckListTemplate.objects.get(id=checklist_id)
    if checklist.directory.owner == owner:
        checklist.directory = Directory.objects.get(id=target_directory_id, owner=owner)
        checklist.save()
        return True
    return False


def move_checklist_up_from_directory(owner: User, checklist_id: int, current_directory_id: int) -> bool:
    """
    Move a checklist up from a current directory with checking of their owner.

    :param owner: a user of an auth user type.
    :param checklist_id: a moving checklist ID.
    :param current_directory_id: a current directory ID.
    :return: True if everything is OK, else - False
    """
    target_directory_id = Directory.objects.get(id=current_directory_id, owner=owner).parent.id
    if move_checklist_into_directory(owner=owner, checklist_id=checklist_id, target_directory_id=target_directory_id):
        return True
    return False


def get_directory_path(owner: User, directory_id: int) -> str:
    """
    Return a full path of a directory with separators - '/'.

    :param owner: a user of an auth user type.
    :param directory_id: a directory id.
    :return: full a full path of a directory.
    """
    parent_directory_path = '/'
    flag = True if directory_id else False
    while flag:
        directory = get_directory(owner=owner, directory_id=directory_id)
        if not directory:
            return ''
        elif directory['parent']:
            parent_directory_path = '/' + directory['name'] + parent_directory_path
            directory_id = directory['parent']
        else:
            flag = False
    return parent_directory_path


def get_json_directory_content(owner: User, directory_id: int):
    """
    Return a directory content in a JSON format with keys:
    'parent_directory' - a parent directory dict with two keys: 'id', 'name',
        where 'name' is a full path to a directory.
    'directories' - consists of a numbered dict,
        where elements are child directory dicts with an ID('id') and a name ('name');
    'checklists' - consists of a numbered dict,
        where elements are child checklist dicts with an ID('id') and a name ('name');

    :param owner: a user of an auth user type.
    :param directory_id: a directory id.
    :return: JSON with two keys: 'directories', 'checklists'.
    """
    parent_directory_path = get_directory_path(owner=owner, directory_id=directory_id)
    parent_directory = {'id': directory_id, 'name': parent_directory_path}
    directory_list = Directory.objects.filter(owner=owner, parent=directory_id).values('id', 'name')
    directory_dict = dict(zip(range(len(directory_list)), directory_list))
    checklist_list = get_checklists_by_directory(owner=owner, directory_id=directory_id)
    checklist_dict = dict(zip(range(len(checklist_list)), checklist_list))
    response = {'parent_directory': parent_directory, 'directories': directory_dict, 'checklists': checklist_dict}
    return response


def add_new_directory(new_directory_name: str, parent_directory_id: int | None, owner: User) -> dict:
    """
    Add a new directory into a checked parent directory of current user.

    :param new_directory_name: a name of a new directory.
    :param parent_directory_id: an ID of a parent directory.
    :param owner: a user of an auth user type.
    :return: a dict with keys: 'id', 'name' of a new directory.
    """
    new_directory = Directory(name=new_directory_name,
                              parent=Directory.objects.get(id=parent_directory_id),
                              owner=owner)
    new_directory.save()
    return {'id': new_directory.pk, 'name': new_directory.name}


def add_new_checklist(new_checklist_name: str, parent_id: int, owner: User):
    """
    Add a new checklist into a checked parent directory of current user.

    :param new_checklist_name: a name of a new checklist.
    :param parent_id: an ID of a parent directory.
    :param owner: a user of an auth user type.
    :return: nothing.
    """
    directory = Directory.objects.get(id=parent_id, owner=owner)
    CheckListTemplate(name=new_checklist_name, directory=directory).save()


def get_existed_checklist_by_owner(checklist_id: int, owner: User) -> dict:
    """
    Get a checklist after checking it belongs to an owner.

    :param checklist_id: an ID of a checklist.
    :param owner: a user of an auth user type.
    :return: a dict with keys: 'id', 'name', 'data'.
    """
    if CheckListTemplate.objects.filter(id=checklist_id) \
            and CheckListTemplate.objects.get(id=checklist_id).directory.owner == owner:
        checklist_data = CheckListTemplate.objects.filter(id=checklist_id).values('id', 'name', 'data')
        if checklist_data:
            return checklist_data[0]
    return {}


def update_checklist_data(checklist_id: int, owner: User, name=None, data=None):
    """
    Update a checklist after checking it belongs to an owner.

    :param checklist_id: an ID of a checklist.
    :param owner: a user of an auth user type.
    :param name: if it is set, replaces checklist 'name'
    :param data: if it is set, replaces checklist 'data'
    :return: a dict with keys: 'id', 'name', 'data'.
    """
    if CheckListTemplate.objects.filter(id=checklist_id) \
            and CheckListTemplate.objects.get(id=checklist_id).directory.owner == owner:
        checklist = CheckListTemplate.objects.get(id=checklist_id)
        if name:
            checklist.name = name
        if data:
            checklist.data = data
        checklist.save()
        return True
    return False


def delete_existed_checklist_by_owner(checklist_id: int, owner: User) -> bool:
    """
    Delete a checklist after checking it belongs to an owner.

    :param checklist_id: an ID of a deleting checklist.
    :param owner: a user of an auth user type.
    :return: True, if a checklist was found and deleted, False if not.
    """
    if CheckListTemplate.objects.filter(id=checklist_id) \
            and CheckListTemplate.objects.get(id=checklist_id).directory.owner == owner:
        result = CheckListTemplate.objects.get(id=checklist_id).delete()
        if result:
            return True
    return False


def delete_directory_by_owner(directory_id: int, owner: User) -> bool:
    """
    Delete a directory after checking it belongs to an owner using a recursive function.

    :param directory_id: an ID of a deleting directory.
    :param owner: a user of an auth user type.
    :return: True, if the directory was found and deleted, False if not.
    """
    if get_directory(owner=owner, directory_id=directory_id):
        result = Directory.objects.get(id=directory_id).delete()
        if result:
            return True
    return False


def get_handler(request: Request):
    """
    Finds known request GET params and processes them.

    :param request: JSON(ajax) request from front-end.
    :return: JSON(ajax) response.
    """
    # Enter into the directory
    try:
        if 'directory_id' in request.GET and request.GET['directory_id'].isdigit():
            json_response = get_json_directory_content(owner=request.user,
                                                       directory_id=int(request.GET['directory_id']))
            return JsonResponse(json_response, status=200)
        # Enter into the parent directory
        elif 'parent_id' in request.GET and request.GET['parent_id'].isdigit():
            directory_id = int(request.GET['parent_id'])
            directory = get_directory(owner=request.user, directory_id=directory_id)
            if directory and directory['parent']:
                directory_id = directory['parent']
            json_response = get_json_directory_content(owner=request.user, directory_id=directory_id)
            return JsonResponse(json_response, status=200)
        elif 'checklist_id' in request.GET and request.GET['checklist_id'].isdigit():
            json_response = get_existed_checklist_by_owner(checklist_id=int(request.GET['checklist_id']),
                                                           owner=request.user)
            if json_response:
                return JsonResponse(json_response, status=200)
        return JsonResponse({'error': 'Error of parameters'}, status=500)
    except Exception as e:
        return JsonResponse({'error': e}, status=500)


def post_handler(request):
    """
    Finds known request POST params and processes them.

    :param request: JSON(ajax) request from front-end.
    :return: JSON(ajax) response.
    """
    # creation a new directory into the current directory
    try:
        if 'new_directory_name' in request.POST and 'current_directory_id' in request.POST \
                and request.POST['current_directory_id'].isdigit():
            parent_directory_id = int(request.POST['current_directory_id'])
            if parent_directory_id == 0 or get_directory(request.user, directory_id=parent_directory_id):
                add_new_directory(new_directory_name=request.POST['new_directory_name'],
                                  parent_directory_id=parent_directory_id,
                                  owner=request.user)
                json_response = get_json_directory_content(owner=request.user, directory_id=parent_directory_id)
                return JsonResponse(json_response, status=200)
        # creation a new checklist into the current directory
        elif 'new_checklist_name' in request.POST and 'current_directory_id' in request.POST \
                and request.POST['current_directory_id'].isdigit():
            parent_directory_id = int(request.POST['current_directory_id'])
            if parent_directory_id == 0 or get_directory(request.user, directory_id=parent_directory_id):
                add_new_checklist(new_checklist_name=request.POST['new_checklist_name'],
                                  parent_id=parent_directory_id,
                                  owner=request.user)
                json_response = get_json_directory_content(owner=request.user, directory_id=parent_directory_id)
                return JsonResponse(json_response, status=200)
        # deletion the directory
        elif 'delete_directory_id' in request.POST and request.POST['delete_directory_id'].isdigit():
            delete_directory_by_owner(directory_id=request.POST['delete_directory_id'], owner=request.user)
            return JsonResponse({'status': 'Success'}, status=200)
        # deletion the checklist
        elif 'delete_checklist_id' in request.POST and request.POST['delete_checklist_id'].isdigit():
            delete_existed_checklist_by_owner(checklist_id=request.POST['delete_checklist_id'], owner=request.user)
            return JsonResponse({'status': 'Success'}, status=200)
        # update checklist information
        elif 'updated_checklist_id' in request.POST and request.POST['updated_checklist_id'].isdigit():
            if update_checklist_data(checklist_id=int(request.POST["updated_checklist_id"]),
                                     owner=request.user,
                                     name=request.POST["checklist_name"],
                                     data=request.POST["checklist_data"]):
                return JsonResponse({'status': 'Success'}, status=200)
        # update directory name
        elif 'updated_directory_id' in request.POST and request.POST['updated_directory_id'].isdigit():
            if update_directory_data(owner=request.user,
                                     directory_id=int(request.POST["updated_directory_id"]),
                                     directory_name=request.POST["directory_name"]):
                return JsonResponse({'status': 'Success'}, status=200)
        # move directory one level up
        elif 'moving_directory_id' in request.POST and request.POST['moving_directory_id'].isdigit() \
                and 'current_directory_id' in request.POST and request.POST['current_directory_id'].isdigit():
            if move_directory_up_from_current_directory(owner=request.user,
                                                        directory_id=int(request.POST["moving_directory_id"]),
                                                        current_directory_id=int(request.POST["current_directory_id"])):
                return JsonResponse({'status': 'Success'}, status=200)
        # update a parent directory of a directory
        elif 'moving_directory_id' in request.POST and request.POST['moving_directory_id'].isdigit() \
                and 'target_directory_id' in request.POST and request.POST['target_directory_id'].isdigit():
            if update_directory_data(owner=request.user,
                                     directory_id=int(request.POST["moving_directory_id"]),
                                     parent_directory_id=int(request.POST["target_directory_id"])):
                return JsonResponse({'status': 'Success'}, status=200)
        # move checklist one level up
        elif 'moving_checklist_id' in request.POST and request.POST['moving_checklist_id'].isdigit() \
                and 'current_directory_id' in request.POST and request.POST['current_directory_id'].isdigit():
            if move_checklist_up_from_directory(owner=request.user,
                                                checklist_id=int(request.POST["moving_checklist_id"]),
                                                current_directory_id=int(request.POST["current_directory_id"])):
                return JsonResponse({'status': 'Success'}, status=200)
        # update a parent directory of a checklist
        elif 'moving_checklist_id' in request.POST and request.POST['moving_checklist_id'].isdigit() \
                and 'target_directory_id' in request.POST and request.POST['target_directory_id'].isdigit():
            if move_checklist_into_directory(owner=request.user,
                                             checklist_id=int(request.POST["moving_checklist_id"]),
                                             target_directory_id=int(request.POST["target_directory_id"])):
                return JsonResponse({'status': 'Success'}, status=200)
        # return JsonResponse({'status': 'Success'}, status=200)
        return JsonResponse({'error': 'Error of parameters'}, status=500)
    except Exception as e:
        return JsonResponse({'error': e}, status=500)
