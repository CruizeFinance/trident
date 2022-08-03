from django.shortcuts import render

# Create your views here.
from rest_framework import status
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from services import DydxAdmin


class User(GenericViewSet):
    def position_id(self, request):

        result = {"message": None, "error": None}
        admin = DydxAdmin()
        try:
            position_id = admin.get_position_id()
            result["message"] = {"position_id": position_id}
            return Response(result, status.HTTP_200_OK)
        except Exception as e:
            result["error"] = str(e)
            return Response(result, status.HTTP_500_INTERNAL_SERVER_ERROR)
