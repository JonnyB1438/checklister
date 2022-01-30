from django.shortcuts import render
from .services import *


# Create your views here.
def index(request):
    """
    The main view of application checks an auth and type of request and sends it to the appropriate handler:
    a built-in template engine or an ajax handler(GET or POST).

    :param request: a request from front-end.
    """
    if request.user.is_authenticated:
        print(f'User: {request.user.username}')
        if request.is_ajax():
            print('------------------AJAX------------------')
            if request.GET:
                return get_handler(request=request)
            elif request.POST:
                return post_handler(request=request)
            else:
                return JsonResponse({'error': 'Error'}, status=500)
        else:
            print('------------------LOAD------------------')
            root_directory = get_root_directory(owner=request.user)
            content = get_json_directory_content(owner=request.user, directory_id=root_directory["id"])
            return render(request, 'checklist/checklist.html', {'content': content})
    return render(request, 'checklist/index.html')  # TODO change to redirection on a login page


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
