from django.shortcuts import render
from django.views import View

from .services import *


class AjaxHandlerView(View):
    #     """
    #     The main view class of application checks an auth and type of request and sends it to the appropriate handler:
    #     a built-in template engine or an ajax handler(GET or POST).
    #     """

    def get(self, request):
        if request.user.is_authenticated:
            if request.is_ajax():
                return get_handler(request=request)
            else:
                root_directory = get_root_directory(owner=request.user)
                content = get_json_directory_content(owner=request.user, directory_id=root_directory["id"])
                return render(request, 'checklist/checklist.html', {'content': content})
        return render(request, 'checklist/index.html')

    def post(self, request):
        if request.user.is_authenticated:
            if request.is_ajax():
                return post_handler(request=request)
            else:
                return JsonResponse({'error': 'Error'}, status=500)
        return render(request, 'checklist/index.html')
