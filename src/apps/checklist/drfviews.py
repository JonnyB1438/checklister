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

    def perform_update(self, serializer):
        if serializer.validated_data['directory'].owner != self.request.user:
            raise PermissionDenied(detail=None, code=None)
        print(serializer.validated_data)
        serializer.save()


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

    def perform_update(self, serializer):
        if serializer.validated_data['parent'].owner != self.request.user:
            raise PermissionDenied(detail=None, code=None)
        serializer.save()


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
