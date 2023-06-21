from cocolife.models import CLAdvertisements
from cocolife.serializers.AdvertisementSerializer import DigiAdvertisementSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from django.db.models import Count
from django.shortcuts import get_object_or_404
from django.views.decorators.csrf import csrf_exempt

__all__ = ['NewsFeedList', 'NewsFeedDetailed',
           'LikedNewsFeedList', 'like_post']


class NewsFeedList(APIView):

    permission_classes = (AllowAny, )

    def get(self, request):
        queryset = CLAdvertisements.objects.all().order_by('publish_date')
        serializer = DigiAdvertisementSerializer(queryset, many=True)
        likes_per_post = CLAdvertisements.objects.all().values(
            'id'
        ).annotate(like_count=Count('liked'))
        context = {
            'advertisement': serializer.data,
            'like_count': likes_per_post
        }
        return Response(context)


class NewsFeedDetailed(APIView):

    permission_classes = (AllowAny,)

    def get(self, request, id):
        
        try:
            queryset = CLAdvertisements.objects.all().filter(id=id)
            view_count = CLAdvertisements.objects.values('view_count').filter(id=id)
            new_count = CLAdvertisements.objects.all().filter(id=id).update(view_count=view_count[0]['view_count'] + 1)
            like_count = CLAdvertisements.objects.all().values(
                'id', 'liked').filter(id=id).aggregate(like_count=Count('liked'))
            serializer = DigiAdvertisementSerializer(queryset, many=True)
            context = {
                "advertisement": serializer.data,
                "like_count": like_count
            }
            return Response(context)
        except IndexError:
            return Response({'error': 'newsfeed does not exists'})


class LikedNewsFeedList(APIView):

    permission_classes = (AllowAny, )

    def get(self, request, id):
        queryset = CLAdvertisements.objects.all().filter(liked=id)
        serializer = DigiAdvertisementSerializer(queryset, many=True)
        return Response({"liked posts": serializer.data})
   

@csrf_exempt
@api_view(["GET", "POST", "PUT"])
@permission_classes([AllowAny])
def like_post(request, advertisement_id, user_id):
    string = ""
    post = get_object_or_404(CLAdvertisements, id=advertisement_id)

    if post.liked.filter(user_id=user_id).exists():
        post.liked.remove(user_id)
        string = "Unliked"
    else:
        post.liked.add(user_id)
        string = "Liked"
    post.save()
    return Response(string)
