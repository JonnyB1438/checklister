from rest_framework import serializers
from .models import Directory, CheckListTemplate


class DirectoryBaseSerializer(serializers.ModelSerializer):
    """'Directory' serializer with minimum data for lists"""
    owner = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = Directory
        fields = ('id', 'name', 'owner',)


class ChecklistBaseSerializer(serializers.ModelSerializer):
    """'CheckListTemplate' serializer with minimum data for lists"""

    class Meta:
        model = CheckListTemplate
        fields = ('id', 'name', )


class ChecklistSerializer(serializers.ModelSerializer):
    """'CheckListTemplate' serializer for RUD actions"""
    class Meta:
        model = CheckListTemplate
        fields = '__all__'


class DirectorySerializer(DirectoryBaseSerializer):
    """'Directory' serializer for RUD actions"""
    checklists = ChecklistBaseSerializer(many=True, read_only=True)
    directories = DirectoryBaseSerializer(many=True, read_only=True)

    class Meta:
        model = Directory
        fields = '__all__'


class RecursiveSerializer(serializers.ModelSerializer):
    """Recursive serializer"""
    def to_representation(self, instance):
        serializer = self.parent.parent.__class__(instance, context=self.context)
        return serializer.data


class DirectoryStructureSerializer(DirectorySerializer):
    """'Directory' serializer for RUD actions"""
    directories = RecursiveSerializer(many=True, read_only=True)

    class Meta:
        model = Directory
        fields = '__all__'
