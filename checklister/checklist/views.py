from django.shortcuts import render
from django.http.response import JsonResponse
from .services import *


# Create your views here.
def index(request):
    if request.user.is_authenticated:
        print(f'User: {request.user.username}')
        if request.is_ajax():
            print('------------------AJAX------------------')
            if request.GET:
                print(f'Request GET: {request.GET}')
                if 'element_id' in request.GET and request.GET['element_id'].isdigit():
                    directory_id = int(request.GET['element_id'])
                    if get_directory(owner=request.user, directory_id=directory_id):
                        if 'go_level_up' in request.GET and request.GET['go_level_up']:
                            if get_directory(owner=request.user, directory_id=directory_id)['parent']:
                                directory_id = get_directory(owner=request.user, directory_id=directory_id)['parent']
                        print(f'Directory id: {directory_id}')
                        json_response = get_directory_list_ajax(user=request.user, directory_id=directory_id)
                        print(f'Json response: {json_response}')
                        return JsonResponse(json_response, status=200)
                return JsonResponse({'error': 'Error'}, status=500)
            elif request.POST:
                print(f'Request POST: {request.POST}')
                if 'new_directory_name' in request.POST and 'current_directory_id' in request.POST:
                    if request.POST['current_directory_id'].isdigit():
                        parent_directory_id = int(request.POST['current_directory_id'])
                        if parent_directory_id == 0 or get_directory(request.user, directory_id=parent_directory_id):
                            add_new_directory(new_directory_name=request.POST['new_directory_name'],
                                              parent_id=parent_directory_id,
                                              owner=request.user)
                            json_response = get_directory_list_ajax(user=request.user, directory_id=parent_directory_id)
                            print(f'Json response: {json_response}')
                            return JsonResponse(json_response, status=200)
                elif 'new_checklist_name' in request.POST and 'current_directory_id' in request.POST:
                    if request.POST['current_directory_id'].isdigit():
                        parent_directory_id = int(request.POST['current_directory_id'])
                        if parent_directory_id == 0 or get_directory(request.user, directory_id=parent_directory_id):
                            add_new_checklist(new_checklist_name=request.POST['new_checklist_name'],
                                  parent_id=parent_directory_id,
                                  owner=request.user)
                            json_response = get_directory_list_ajax(user=request.user, directory_id=parent_directory_id)
                            print(f'Json response: {json_response}')
                            return JsonResponse(json_response, status=200)
                elif 'directory_id' in request.POST and request.POST['directory_id'].isdigit():
                    if get_directory(request.user, directory_id=request.POST['directory_id']):
                        if 'checklist' in request.POST and request.POST['checklist'].isdigit():
                            if is_checklist(id=request.POST['checklist'], directory=request.POST['directory_id']):
                                delete_checklist(id=request.POST['checklist'])
                                return JsonResponse({'status': 'Success'}, status=200)
                        else:
                            delete_directory(id=request.POST['directory_id'])
                            return JsonResponse({'status': 'Success'}, status=200)
                return JsonResponse({'error': 'Error'}, status=500)
            else:
                return JsonResponse({'error': 'Error'}, status=500)
        else:
            print('------------------LOAD------------------')
            root_directory = get_directories_by_parent(owner=request.user, parent_id=0)
            if not root_directory:
                root_directory = add_new_directory(new_directory_name='/', parent_id=0, owner=request.user)
            else:
                root_directory = root_directory[0]
            directory_list = get_directories_by_parent(owner=request.user, parent_id=root_directory["id"])
            directory_checklists = get_directory_checklists(owner=request.user, directory_id=root_directory["id"])
            return render(request, 'checklist/checklist.html', {'root_directory': {'id': root_directory['id'],
                                                                                   'name': root_directory['name']},
                                                                'directory_list': directory_list,
                                                                'checklist_list': directory_checklists})
    return render(request, 'checklist/checklist.html') # TODO change to redirection on a login page


# class AjaxHandlerView(View):
#     def get(self, request):
#         text = request.GET.get('element_text')
#         print()
#         print(text)
#         print()
#         if request.is_ajax():
#             t = time()
#             return JsonResponse({'seconds':t}, status=200)
#         return render(request, 'checklist/checklist.html')
