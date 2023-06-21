from cocolife.serializers import FeatureSerializer
from cocolife.models.Feature import CLFeature

from rest_framework.generics import RetrieveUpdateDestroyAPIView, ListCreateAPIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny

__all__ = ['Features', 'FeaturesById']


class Features(ListCreateAPIView):
    # TODO - Make Authenticated
    permission_classes = (AllowAny,)
    queryset = CLFeature.objects.all()
    serializer_class = FeatureSerializer

    def get_queryset(self):
        qs = super().get_queryset()
        type = self.request.query_params.get('client_type')
        if type:
            qs = qs.filter(client_type=type)
        return qs


class FeaturesById(RetrieveUpdateDestroyAPIView):
    permission_classes = (AllowAny,)
    lookup_field = 'id'
    queryset = CLFeature.objects.all()
    serializer_class = FeatureSerializer
