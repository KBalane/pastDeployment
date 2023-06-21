from rest_framework.views import APIView
from rest_framework.response import Response
from api.serializers import URLSerializer
from rest_framework.permissions import AllowAny

from bs4 import BeautifulSoup
from urllib.request import urlopen

__all__ = ['ExtractURL']


def get_meta_details(meta, property_name, default_value=""):
        if "property" in meta.attrs and meta.attrs['property']== property_name:
            return meta.attrs['content']
        return default_value
class ExtractURL(APIView):
    """
    Sample Request:
    http://digiinsurance.qymera.tech/api/v1/ad/extracturl/?link=https://www.insider.com/who-has-been-sexiest-man-alive-people-2018-11
    """
    permission_classes = [AllowAny]
    serializer_class = URLSerializer

    def get(self, request,*args, **kwargs):
        #external_url = "https://www.insider.com/who-has-been-sexiest-man-alive-people-2018-11"
        external_url = request.GET.get('link')
        external_site_html = urlopen(external_url).read()
        soup = BeautifulSoup(external_site_html, "html.parser")

        title = soup.title.text
        image = ""
        description = ""

        for meta in soup.findAll("meta"):
            title = get_meta_details(meta, "og:title", title)
            image = get_meta_details(meta, "og:image", image)
            description = get_meta_details(meta, "og:description", description)
 
        context = {
            "title":title,
            "image": image,
            "description": description
        }
        return Response(context)

    