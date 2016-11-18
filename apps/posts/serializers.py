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
        fields = ('date_created', 'type', 'themes', 'keywords', 'content',
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
