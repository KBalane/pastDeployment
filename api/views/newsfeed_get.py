from digiinsurance.models import Advertisement
from django.shortcuts import get_object_or_404
from api.serializers import AdvertisementSerializer
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.generics import ListAPIView, RetrieveAPIView, RetrieveUpdateDestroyAPIView
from django.db.models import CharField, Value as V
from django.db.models import Sum, Count
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
from django.views.decorators.csrf import csrf_protect, csrf_exempt
#from rest_framework.decorators import api_view, renderer_classes

__all__ = ['NewsfeedList','NewsfeedDetailed','like_post']

class NewsfeedList(APIView):
    permission_classes = (AllowAny,)
    #lookup_field = 'id'
    def get(self,request):
        queryset = Advertisement.objects.all().order_by('-Publish_Date')

        serializer_class = AdvertisementSerializer(queryset,many=True)

        likes_per_post = Advertisement.objects.all().values(
            'id'
        ).annotate(like_count = Count('liked'))

        context = {
            "posts": serializer_class.data,
            #"like_count_per_post": likes_per_post,
        }
        return Response(context)


class NewsfeedDetailed(APIView):
    permission_classes = (AllowAny,)
    def get(self, request, pk):
        queryset = Advertisement.objects.all().filter(id = pk)
        # Find companies that have more employees than chairs.
        like_count = Advertisement.objects.all().values(
            'id','liked'
            ).filter(id = pk).aggregate(like_count = Count('liked'))
        
        serializer_class = AdvertisementSerializer(queryset, many=True)
        context = {
            "advertisement":serializer_class.data,
            "like_count":like_count
        }
        return Response(context)

#@renderer_classes([renderers.OpenAPIRenderer, renderers.SwaggerUIRenderer])
@csrf_exempt
@api_view(["GET","POST","PUT"])
@permission_classes([AllowAny])
def like_post(request, advertisement_id, user_id): #TODO - Rewrite Endpoint
    string = ""
    post = get_object_or_404(Advertisement, id = advertisement_id)

    if post.liked.filter(id = user_id).exists():
        post.liked.remove(user_id)
        string = "Unliked"
    else:
        post.liked.add(user_id)
        string = "Liked"
    post.save()
    return HttpResponse(string)




"""
def like_post(request, user_id, advertisement_id):
    if request.method == 'POST':
        advertisement_obj = Advertisement.objects.get(id = advertisement_id)

        if user_id in advertisement_obj.Liked.all():
            advertisement_obj.Liked.remove(user_id)
        else:
            advertisement_obj.Liked.add(user_id)
        
        like, created = Like.objects.get_or_create(user = user_id, advertisement = advertisement_id)

        if not created:
            if like.value == 'Like':
                like.value = 'Unlike'
            else:
                like.value = 'Like'
        
        like.save()
        return Response(like)

def like(request, user_id, picture_id):
    new_like, created = Like.objects.get_or_create(user=user_id, picture_id=picture_id)
    if not created:
        # the user already liked this picture before
    else:
        # oll korrekt

def picture_detail(request, id):
    pic = get_object_or_404(Picture, pk=id)
    user_likes_this = pic.like_set.filter(user=request.user) and True or False
"""
