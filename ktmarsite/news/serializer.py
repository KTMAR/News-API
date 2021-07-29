from django.contrib.auth.models import User
from rest_framework import serializers
from rest_framework.serializers import ModelSerializer

from news.models import News, UserNewsRelation



class BookReadersSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ('first_name', 'last_name')

class NewsSerializer(ModelSerializer):
    annotated_likes = serializers.IntegerField(read_only=True)
    rating = serializers.DecimalField(max_digits=3, decimal_places=2, read_only=True)
    owner_name = serializers.CharField(source='owner_name.username', default='', read_only=True)

    readers = BookReadersSerializer(many=True)

    class Meta:
        model = News
        fields = ('id', 'title', 'owner_name', 'content', 'photo', 'cat',
                  'annotated_likes', 'rating', 'owner_name', 'readers')




class UserNewsRelationSerializer(ModelSerializer):
    class Meta:
        model = UserNewsRelation
        fields = ('news', 'like', 'rate')
