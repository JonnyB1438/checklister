from rest_framework.exceptions import PermissionDenied
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView, GenericAPIView
from rest_framework.response import Response

from .models import Directory, CheckListTemplate
from .serializers import *
from .permissions import *
from .services import get_directory


class ChecklistListAPIView(ListCreateAPIView):
    """Get current user checklists from a directory by id or create a checklist in this directory"""
    serializer_class = ChecklistBaseSerializer

    def get_queryset(self):
        return CheckListTemplate.objects.filter(directory_id=self.kwargs.get('dir_id'),
                                                directory__owner=self.request.user)

    def perform_create(self, serializer):
        if get_directory(directory_id=self.kwargs.get('dir_id'), owner=self.request.user):
            return serializer.save(directory_id=self.kwargs.get('dir_id'))
        else:
            raise PermissionDenied(detail=None, code=None)


class ChecklistRUDAPIView(RetrieveUpdateDestroyAPIView):
    """Get, modify and delete current user checklist by id"""
    serializer_class = ChecklistSerializer

    def get_queryset(self):
        return CheckListTemplate.objects.filter(pk=self.kwargs.get('pk'),
                                                directory__owner=self.request.user)

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        if not get_directory(directory_id=int(self.request.POST.get('directory')), owner=self.request.user):
            raise PermissionDenied(detail=None, code=None)
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        if getattr(instance, '_prefetched_objects_cache', None):
            instance._prefetched_objects_cache = {}
        return Response(serializer.data)


class DirectoryListAPIView(ListCreateAPIView):
    """Get current user directories from their parent directory by parent directory id
    or create a new directory there"""
    serializer_class = DirectoryBaseSerializer

    def get_queryset(self):
        return Directory.objects.filter(parent=self.kwargs.get('parent_id'),
                                        owner=self.request.user)

    def perform_create(self, serializer):
        if get_directory(directory_id=self.kwargs.get('parent_id'), owner=self.request.user):
            return serializer.save(parent_id=self.kwargs.get('parent_id'))
        raise PermissionDenied(detail=None, code=None)


class DirectoryRUDAPIView(RetrieveUpdateDestroyAPIView):
    """Get, modify and delete current user directory by id"""
    serializer_class = DirectorySerializer
    # permission_classes = (IsOwner, )

    def get_queryset(self):
        return Directory.objects.filter(owner=self.request.user, pk=self.kwargs.get('pk'))\
            .prefetch_related('checklists')\
            .prefetch_related('directories')

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        if not get_directory(directory_id=int(self.request.POST.get('parent')), owner=self.request.user):
            raise PermissionDenied(detail=None, code=None)
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        if getattr(instance, '_prefetched_objects_cache', None):
            instance._prefetched_objects_cache = {}
        return Response(serializer.data)


class DirectoryAPIView(GenericAPIView):
    """Get directory by id with all subdirectories and checklists"""
    serializer_class = DirectoryStructureSerializer

    def get(self, request, *args, **kwargs):
        queryset = Directory.objects\
            .prefetch_related('directories')\
            .prefetch_related('checklists')\
            .get(parent=None, owner=self.request.user)
        serializer = self.get_serializer(queryset)
        return Response(serializer.data)
