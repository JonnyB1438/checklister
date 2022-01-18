from django.http.response import JsonResponse

from .models import Directory, CheckListTemplate


def get_directory(owner, directory_id: int) -> dict:
    """
    Performs a secure existence check of the directory by owner (using filter method).

    :param owner: a user of an auth user type.
    :param directory_id: a checking directory id.
    :return: An empty dictionary or a dictionary with keys 'id', 'name' and 'parent' of founded directory.
    """
    directory_response = Directory.objects.filter(owner=owner, id=directory_id).values('id', 'name', 'parent')
    directory_response = directory_response[0] if directory_response else {}
    return directory_response


def get_root_directory(owner) -> dict:
    """
    Check an auth user root directory, if it does not exist, create it.
    Return a dict with keys: 'id', 'name' of the root directory.

    :param owner: a user of an auth user type.
    :return: a dict with keys: 'id', 'name' of the root directory.
    """
    root_directory = Directory.objects.filter(owner=owner, parent=0).values('id', 'name')
    if not root_directory:
        root_directory = add_new_directory(new_directory_name='/', parent_id=0, owner=owner)
    else:
        root_directory = root_directory[0]
    return root_directory


def get_checklists_by_directory(owner, directory_id: int) -> list:
    """
    Return a list of checklists in the owner directory as dictionaries with keys: 'id', 'name'.

    :param owner: a user of an auth user type.
    :param directory_id: a search directory id.
    :return: a list of dictionaries with keys: 'id', 'name'.
    """
    directory = Directory.objects.get(id=directory_id, owner=owner)
    return CheckListTemplate.objects.filter(directory=directory).values('id', 'name')


def get_directory_path(owner, directory_id: int) -> str:
    """
    Return a full path of the directory with separators - '/'.

    :param owner: a user of an auth user type.
    :param directory_id: a directory id.
    :return: full a full path of the directory.
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


def get_json_directory_content(owner, directory_id: int):
    """
    Return directory content in a JSON format with keys:
    'parent_directory' - a parent directory dict with two keys: 'id', 'name',
        where 'name' is a full path to the directory.
    'directories' - consists of a numbered dict,
        where elements are child directory dicts with an ID('id') and a name ('name');
    'checklists' - consists of a numbered dict,
        where elements are child checklist dicts with an ID('id') and a name ('name');

    :param owner: a user of an auth user type.
    :param directory_id: a directory id.
    :return: JSON with two keys: 'directories', 'checklists'.
    """
    print("Get JSON directory list")
    parent_directory_path = get_directory_path(owner=owner, directory_id=directory_id)
    print(f'Parent dir_path: {parent_directory_path}')
    parent_directory = {'id': directory_id, 'name': parent_directory_path}
    directory_list = Directory.objects.filter(owner=owner, parent=directory_id).values('id', 'name')
    directory_dict = dict(zip(range(len(directory_list)), directory_list))
    checklist_list = get_checklists_by_directory(owner=owner, directory_id=directory_id)
    checklist_dict = dict(zip(range(len(checklist_list)), checklist_list))
    response = {'parent_directory': parent_directory, 'directories': directory_dict, 'checklists': checklist_dict}
    return response


def add_new_directory(new_directory_name: str, parent_id: int, owner) -> dict:
    """
    Add a new directory into the checked parent directory of the current user.

    :param new_directory_name: the name of a new directory.
    :param parent_id: the ID of the parent directory.
    :param owner: a user of an auth user type.
    :return: a dict with keys: 'id', 'name' of the new directory.
    """
    new_directory = Directory(name=new_directory_name, parent=parent_id, owner=owner)
    new_directory.save()
    return {'id': new_directory.pk, 'name': new_directory.name}


def add_new_checklist(new_checklist_name: str, parent_id: int, owner):
    """
    Add a new checklist into the checked parent directory of the current user.

    :param new_checklist_name: the name of a new checklist.
    :param parent_id: the ID of the parent directory.
    :param owner: a user of an auth user type.
    :return: nothing.
    """
    directory = Directory.objects.get(id=parent_id, owner=owner)
    CheckListTemplate(name=new_checklist_name, directory=directory).save()


def get_existed_checklist_by_owner(checklist_id: int, owner) -> dict:
    """
    Get the checklist after checking that it belongs to the owner.

    :param checklist_id: an ID of the checklist.
    :param owner: a user of an auth user type.
    :return: a dict with keys: 'id', 'name', 'data'.
    """
    if CheckListTemplate.objects.filter(id=checklist_id) \
            and CheckListTemplate.objects.get(id=checklist_id).directory.owner == owner:
        checklist_data = CheckListTemplate.objects.filter(id=checklist_id).values('id', 'name', 'data')
        if checklist_data:
            return checklist_data[0]
    return {}


def delete_existed_checklist_by_owner(checklist_id: int, owner) -> bool:
    """
    Delete the checklist after checking that it belongs to the owner.

    :param checklist_id: an ID of the deleting checklist.
    :param owner: a user of an auth user type.
    :return: True, if the checklist was found and deleted, False if not.
    """
    if CheckListTemplate.objects.filter(id=checklist_id) \
            and CheckListTemplate.objects.get(id=checklist_id).directory.owner == owner:
        CheckListTemplate.objects.get(id=checklist_id).delete()
        return True
    return False


def delete_directory_by_owner(directory_id: int, owner) -> bool:
    """
    Delete a directory after checking that it belongs to the owner using a recursive function.

    :param directory_id: an ID of the deleting directory.
    :param owner: a user of an auth user type.
    :return: True, if the directory was found and deleted, False if not.
    """
    if get_directory(owner=owner, directory_id=directory_id):
        delete_directory_recursively(directory_id=directory_id)
        return True
    return False


def delete_directory_recursively(directory_id: int):
    """
    Delete a directory by using recursion. Find children and run itself for everyone of them.

    :param directory_id: an ID of the deleting directory.
    :return: nothing
    """
    child_directories = Directory.objects.filter(parent=directory_id).values('id')
    if child_directories:
        for child_directory in child_directories:
            delete_directory_recursively(directory_id=child_directory['id'])
    Directory.objects.filter(id=directory_id).delete()


def get_handler(request):
    """
    Finds known request GET params and processes them.

    :param request: JSON(ajax) request from front-end.
    :return: JSON(ajax) response.
    """
    print(f'Request GET: {request.GET}')
    # Enter into the directory
    if 'directory_id' in request.GET and request.GET['directory_id'].isdigit():
        json_response = get_json_directory_content(owner=request.user, directory_id=int(request.GET['directory_id']))
        print(f'Json response: {json_response}')
        return JsonResponse(json_response, status=200)
    # Enter into the parent directory
    elif 'parent_id' in request.GET and request.GET['parent_id'].isdigit():
        directory_id = int(request.GET['parent_id'])
        directory = get_directory(owner=request.user, directory_id=directory_id)
        if directory and directory['parent']:
            directory_id = directory['parent']
        json_response = get_json_directory_content(owner=request.user, directory_id=directory_id)
        print(f'Json response: {json_response}')
        return JsonResponse(json_response, status=200)
    elif 'checklist_id' in request.GET and request.GET['checklist_id'].isdigit():
        json_response = get_existed_checklist_by_owner(checklist_id=int(request.GET['checklist_id']), owner=request.user)
        return JsonResponse(json_response, status=200)
    return JsonResponse({'error': 'Error'}, status=500)


def post_handler(request):
    """
    Finds known request POST params and processes them.

    :param request: JSON(ajax) request from front-end.
    :return: JSON(ajax) response.
    """
    print(f'Request POST: {request.POST}')
    # creation a new directory into the current directory
    if 'new_directory_name' in request.POST and 'current_directory_id' in request.POST \
            and request.POST['current_directory_id'].isdigit():
        parent_directory_id = int(request.POST['current_directory_id'])
        if parent_directory_id == 0 or get_directory(request.user, directory_id=parent_directory_id):
            add_new_directory(new_directory_name=request.POST['new_directory_name'],
                              parent_id=parent_directory_id,
                              owner=request.user)
            json_response = get_json_directory_content(owner=request.user, directory_id=parent_directory_id)
            print(f'Json response: {json_response}')
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
            print(f'JSON response: {json_response}')
            return JsonResponse(json_response, status=200)
    # deletion the directory
    elif 'delete_directory_id' in request.POST and request.POST['delete_directory_id'].isdigit():
        delete_directory_by_owner(directory_id=request.POST['delete_directory_id'], owner=request.user)
        return JsonResponse({'status': 'Success'}, status=200)
    # deletion the checklist
    elif 'delete_checklist_id' in request.POST and request.POST['delete_checklist_id'].isdigit():
        delete_existed_checklist_by_owner(checklist_id=request.POST['delete_checklist_id'], owner=request.user)
        return JsonResponse({'status': 'Success'}, status=200)
    return JsonResponse({'error': 'Error'}, status=500)
