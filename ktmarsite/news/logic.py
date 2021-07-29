from django.db.models import Avg

from news.models import UserNewsRelation


def set_rating(news):
    rating = UserNewsRelation.objects.filter(news=news).aggregate(rating=Avg('rate'))
    news.rating = rating
    news.save()