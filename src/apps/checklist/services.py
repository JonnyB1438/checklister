from django.core.exceptions import ObjectDoesNotExist, MultipleObjectsReturned
from django.http.response import JsonResponse
from requests import Request
from django.contrib.auth.models import User

from .models import Directory, CheckListTemplate


def get_directory(owner: User, directory_id: int) -> dict:
    """
    Performs a secure existence check of a directory by an owner (using filter method).
    :param owner: a user of an auth user type.
    :param directory_id: a checking directory id.
    :return: An empty dictionary or a dictionary with keys 'id', 'name' and 'parent' of founded directory.
    """
    try:
        directory = Directory.objects.select_related('parent').get(owner=owner, id=directory_id)
    except ObjectDoesNotExist:
        return {}
    if directory.parent:
        return {'id': directory.id, 'name': directory.name, 'parent': directory.parent.id}
    else:
        return {'id': directory.id, 'name': directory.name, 'parent': directory.parent}


def get_root_directory(owner: User) -> dict:
    """
    Check an auth user root directory, if it does not exist, create it.
    Return a dict with keys: 'id', 'name' of the root directory.
    :param owner: a user of an auth user type.
    :return: a dict with keys: 'id', 'name' of the root directory.
    """
    try:
        root_directory = Directory.objects.get(owner=owner, parent__isnull=True)
        return {'id': root_directory.id, 'name': root_directory.name}
    except ObjectDoesNotExist:
        return add_new_directory(new_directory_name='/', parent_directory_id=None, owner=owner)
    except MultipleObjectsReturned:
        return Directory.objects.filter(owner=owner, parent__isnull=True).values('id', 'name').first()


def update_directory_data(owner: User, directory_id: int, directory_name=None, parent_directory_id=None) -> bool:
    """
    Change a directory(name, parent) with checking of an owner(directory and parent).
    :param owner: a user of an auth user type.
    :param directory_id: a changing directory ID.
    :param parent_directory_id: a new parent directory ID.
    :param directory_name: a new directory name.
    :return: True if everything is OK, else - False
    """
    if directory_name or parent_directory_id:
        try:
            directory = Directory.objects.get(id=directory_id, owner=owner)
        except ObjectDoesNotExist:
            return False
        if directory_name:
            directory.name = directory_name
        if parent_directory_id:
            try:
                parent_directory = Directory.objects.get(id=parent_directory_id, owner=owner)
            except ObjectDoesNotExist:
                return False
            directory.parent = parent_directory
        directory.save()
    return True


def move_directory_up_from_current_directory(owner: User, directory_id: int, current_directory_id: int) -> bool:
    """
    Move a directory up from a current directory with checking of their owner.
    :param owner: a user of an auth user type.
    :param directory_id: a moving directory ID.
    :param current_directory_id: a current directory ID.
    :return: True if everything is OK, else - False
    """
    try:
        target_directory_id = Directory.objects.get(id=current_directory_id, owner=owner).parent.id
    except ObjectDoesNotExist:
        return False
    return update_directory_data(owner=owner, directory_id=directory_id, parent_directory_id=target_directory_id)


def move_checklist_into_directory(owner: User, checklist_id: int, target_directory_id: int) -> bool:
    """
    Move a checklist to another directory with checking of their owner.
    :param owner: a user of an auth user type.
    :param checklist_id: a moving checklist ID.
    :param target_directory_id: a target directory ID.
    :return: True if everything is OK, else - False
    """
    try:
        target_directory = Directory.objects.get(id=target_directory_id, owner=owner)
    except ObjectDoesNotExist:
        return False
    return CheckListTemplate.objects.filter(id=checklist_id, directory__owner=owner).update(directory=target_directory)


def move_checklist_up_from_directory(owner: User, checklist_id: int, current_directory_id: int) -> bool:
    """
    Move a checklist up from a current directory with checking of their owner.
    :param owner: a user of an auth user type.
    :param checklist_id: a moving checklist ID.
    :param current_directory_id: a current directory ID.
    :return: True if everything is OK, else - False
    """
    try:
        target_directory_id = Directory.objects.select_related('parent').\
            get(id=current_directory_id, owner=owner).parent.id
    except ObjectDoesNotExist or AttributeError:
        return False
    return move_checklist_into_directory(owner=owner,
                                         checklist_id=checklist_id,
                                         target_directory_id=target_directory_id)


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
    Return a directory content in a dict format with keys:
    'parent_directory' - a parent directory dict with two keys: 'id', 'name',
        where 'name' is a full path to a directory.
    'directories' - consists of a numbered dict,
        where elements are child directory dicts with an ID('id') and a name ('name');
    'checklists' - consists of a numbered dict,
        where elements are child checklist dicts with an ID('id') and a name ('name');
    :param owner: a user of an auth user type.
    :param directory_id: a directory id.
    :return: dict with keys: 'parent_directory'('id', 'path'), 'directories', 'checklists'.
    """
    parent_directory_path = get_directory_path(owner=owner, directory_id=directory_id)
    parent_directory = {'id': directory_id, 'name': parent_directory_path}
    directory_list = Directory.objects.filter(owner=owner, parent=directory_id).values('id', 'name')
    directory_dict = {index: directory for index, directory in enumerate(directory_list)}
    checklist_list = CheckListTemplate.objects.filter(directory=directory_id, directory__owner=owner).values('id', 'name')
    checklist_dict = {index: checklist for index, checklist in enumerate(checklist_list)}
    return {'parent_directory': parent_directory, 'directories': directory_dict, 'checklists': checklist_dict}


def add_new_directory(new_directory_name: str, parent_directory_id: int | None, owner: User) -> dict:
    """
    Add a new directory into a checked parent directory of current user.
    :param new_directory_name: a name of a new directory.
    :param parent_directory_id: an ID of a parent directory.
    :param owner: a user of an auth user type.
    :return: a dict with keys: 'id', 'name' of a new directory.
    """
    if parent_directory_id:
        try:
            parent_directory = Directory.objects.get(id=parent_directory_id, owner=owner)
        except ObjectDoesNotExist:
            return {}
    else:
        parent_directory = None
    new_directory = Directory(name=new_directory_name, parent=parent_directory, owner=owner)
    new_directory.save()
    return {'id': new_directory.id, 'name': new_directory.name}


def add_new_checklist(new_checklist_name: str, parent_id: int, owner: User):
    """
    Add a new checklist into a checked parent directory of current user.
    :param new_checklist_name: a name of a new checklist.
    :param parent_id: an ID of a parent directory.
    :param owner: a user of an auth user type.
    :return: nothing.
    """
    try:
        parent_directory = Directory.objects.get(id=parent_id, owner=owner)
    except ObjectDoesNotExist:
        return
    checklist = CheckListTemplate(name=new_checklist_name, directory=parent_directory)
    checklist.save()
    return {'id': checklist.id, 'name': checklist.name}


def get_checklist_data_by_owner(checklist_id: int, owner: User) -> dict:
    """
    Get a checklist after checking it belongs to an owner.
    :param checklist_id: an ID of a checklist.
    :param owner: a user of an auth user type.
    :return: a dict with keys: 'id', 'name', 'data'.
    """
    try:
        checklist_data = CheckListTemplate.objects.get(id=checklist_id, directory__owner=owner)
    except ObjectDoesNotExist:
        return {}
    return {'id': checklist_data.id, 'name': checklist_data.name, 'data': checklist_data.data}


def update_checklist_data(checklist_id: int, owner: User, name=None, data=None):
    """
    Update a checklist after checking it belongs to an owner.
    :param checklist_id: an ID of a checklist.
    :param owner: a user of an auth user type.
    :param name: if it is set, replaces checklist 'name'
    :param data: if it is set, replaces checklist 'data'
    :return: a dict with keys: 'id', 'name', 'data'.
    """
    try:
        checklist = CheckListTemplate.objects.get(id=checklist_id, directory__owner=owner)
    except ObjectDoesNotExist:
        return False
    if name:
        checklist.name = name
    if data:
        checklist.data = data
    checklist.save()
    return True


def delete_checklist_by_owner(checklist_id: int, owner: User) -> bool:
    """
    Delete a checklist after checking it belongs to an owner.
    :param checklist_id: an ID of a deleting checklist.
    :param owner: a user of an auth user type.
    :return: True, if a checklist was found and deleted, False if not.
    """
    try:
        checklist = CheckListTemplate.objects.get(id=checklist_id, directory__owner=owner)
    except ObjectDoesNotExist:
        return False
    return checklist.delete()


def delete_directory_by_owner(directory_id: int, owner: User) -> bool:
    """
    Delete a directory after checking it belongs to an owner using a recursive function.
    :param directory_id: an ID of a deleting directory.
    :param owner: a user of an auth user type.
    :return: True, if the directory was found and deleted, False if not.
    """
    try:
        directory = Directory.objects.get(id=directory_id, owner=owner)
    except ObjectDoesNotExist:
        return False
    return directory.delete()


def get_handler(request: Request):
    """
    Finds known request GET params and handles them.
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
                json_response = get_json_directory_content(owner=request.user, directory_id=directory['parent'])
                return JsonResponse(json_response, status=200)
        # Show checklist
        elif 'checklist_id' in request.GET and request.GET['checklist_id'].isdigit():
            json_response = get_checklist_data_by_owner(checklist_id=int(request.GET['checklist_id']),
                                                        owner=request.user)
            return JsonResponse(json_response, status=200)
        return JsonResponse({'error': 'Error of parameters'}, status=500)
    except Exception as e:
        return JsonResponse({'error': e}, status=500)


def post_handler(request):
    """
    Finds known request POST params and handles them.
    :param request: JSON(ajax) request from front-end.
    :return: JSON(ajax) response.
    """
    # creation a new directory into the current directory
    try:
        if 'new_directory_name' in request.POST and 'current_directory_id' in request.POST \
                and request.POST['current_directory_id'].isdigit():
            parent_directory_id = int(request.POST['current_directory_id'])
            if add_new_directory(new_directory_name=request.POST['new_directory_name'],
                                 parent_directory_id=parent_directory_id,
                                 owner=request.user):
                json_response = get_json_directory_content(owner=request.user, directory_id=parent_directory_id)
                return JsonResponse(json_response, status=200)
        # creation a new checklist into the current directory
        elif 'new_checklist_name' in request.POST \
                and 'current_directory_id' in request.POST \
                and request.POST['current_directory_id'].isdigit():
            parent_directory_id = int(request.POST['current_directory_id'])
            if add_new_checklist(new_checklist_name=request.POST['new_checklist_name'],
                                 parent_id=parent_directory_id,
                                 owner=request.user):
                json_response = get_json_directory_content(owner=request.user, directory_id=parent_directory_id)
                return JsonResponse(json_response, status=200)
        # deletion the directory
        elif 'delete_directory_id' in request.POST and request.POST['delete_directory_id'].isdigit():
            if delete_directory_by_owner(directory_id=request.POST['delete_directory_id'], owner=request.user):
                return JsonResponse({'status': 'Success'}, status=200)
        # deletion the checklist
        elif 'delete_checklist_id' in request.POST and request.POST['delete_checklist_id'].isdigit():
            if delete_checklist_by_owner(checklist_id=request.POST['delete_checklist_id'], owner=request.user):
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
