from rest_framework import serializers
from .models import *


class RepostSerializer(serializers.ModelSerializer):
    # owner = serializers.PrimaryKeyRelatedField(
    #     read_only=True, default=serializers.CurrentUserDefault())
    themes = serializers.ListField(
        child=serializers.CharField(max_length=100, min_length=0))
    keywords = serializers.ListField(
        child=serializers.CharField(max_length=100, min_length=0))

    class Meta:
        model = Post
        fields = ('id', 'date_created', 'type', 'themes', 'keywords', 'content',
                  # 'owner'
                  )

        read_only_fields = ('date_created', )

    # def validate(self, validated_data):
    #     validated_data['owner'] = self.context['request'].user

        # other validation logic, e.g.
        # validated_data['size'] = validated_data['file'].size

        # return validated_data

    # def create(self, validated_data):
        # return Post.objects.create(**validated_data)

class UpdatePostSerializer(serializers.ModelSerializer):
    #owner = serializers.ReadOnlyField(source='owner.username')

    class Meta:
        model = Post
        fields = ('id', 'publish_date',
                'themes', 'keywords', 'content',
                #'owner'
                )

        read_only_fields = ('date_created', )

class CreatePostSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')
    page = serializers.ReadOnlyField(source='page.id')

    publish_date = serializers.DateTimeField(format="%Y-%m-%dT%H:%M:%SZ")

    class Meta:
        model = Post
        fields = ('id', 'publish_date', 'status', "type",
                'themes', 'keywords', 'content',
                'owner', 'page'
                )

        read_only_fields = ('date_created', )

class ShowPostSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')
    page = serializers.ReadOnlyField(source='page.id')

    publish_date = serializers.DateTimeField(format="%Y-%m-%dT%H:%M:%SZ")
    date_created = serializers.DateTimeField(format="%Y-%m-%dT%H:%M:%SZ")

    class Meta:
        ordering = ('publish_date',)
        model = Post
        fields = ('id', 'publish_date', 'status', "type", 'date_created',
                'themes', 'keywords', 'content',
                'owner', 'page'
                )

        read_only_fields = ('date_created', )


class PageSerializer(serializers.ModelSerializer):
    # extra_data = JSONField(binary=True)
    class Meta:
        model = Pages
        fields = ('id', 'uid', 'name', 'avatar', 'provider', 
            'type', 'extra_data')

class ShowPageSerializer(serializers.ModelSerializer):
    # extra_data = JSONField(binary=True)
    class Meta:
        model = Pages
        fields = ('id', 'uid', 'name', 'avatar', 'provider', 
            'type', 'extra_data')

class PageUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = PageUser
        fields = ('id', 'user', 'page')