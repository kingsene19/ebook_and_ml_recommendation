from tokenize import Token
from django.http import JsonResponse
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.response import Response
from .serializers import ProduitSerializer
from .models import Produit
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import BasicAuthentication, TokenAuthentication


@api_view(['GET', 'POST'])
@authentication_classes([BasicAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated])
def rest_api(request):
    if request.method == "GET":
        queryset = Produit.objects.all()
        ser = ProduitSerializer(queryset, many=True)
        return Response(ser.data)
    if request.method == "POST":
        data = request.data
        ser = ProduitSerializer(data=data)
        if ser.is_valid():
            ser.save()
            return JsonResponse(ser.data, status=200)
