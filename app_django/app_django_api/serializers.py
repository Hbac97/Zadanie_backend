from rest_framework import serializers
from .models import Posts

class PostsSerialiser(serializers.ModelSerializer):

    class Meta:
        model = Posts
        fields = ['authors','content']

