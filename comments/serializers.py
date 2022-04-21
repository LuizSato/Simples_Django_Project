from genericpath import exists
from . import models
from rest_framework import serializers

class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Comment
        exclude = ['id']
    
    def validate_user(self, user_id):
        if user_id == None:
            raise serializers.ValidationError('User not found')
        try:
            models.User.objects.get(id=user_id)
        except models.User.DoesNotExist:
            raise serializers.ValidationError('User not found')