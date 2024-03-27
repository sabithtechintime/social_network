from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response


@api_view(['GET'])
def home(request):
    data = {"message": "Yes this is the response"}
    return Response(data)
