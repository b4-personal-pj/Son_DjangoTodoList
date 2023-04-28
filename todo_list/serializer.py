from rest_framework import serializers
from .models import Post




class PostSerializer(serializers.ModelSerializer):
    owner = serializers.SerializerMethodField()
    def get_owner(self, obj):
        return obj.owner.name

    class Meta:
        model = Post
        fields = ('title','owner')


class CreatePostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ('title','comment','is_complete')

class DetailPostSerializer(serializers.ModelSerializer):
    owner = serializers.SerializerMethodField()
    def get_owner(self, obj):
        return obj.owner.name

    class Meta:
        model = Post
        fields = "__all__"
