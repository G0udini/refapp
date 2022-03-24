from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from user.throttles import CustomUserRateThrottle
from user.services import LoginInitialService, LoginCompleteService


class LoginInitial(APIView):
    throttle_classes = [CustomUserRateThrottle]

    def post(self, request):
        if context := LoginInitialService(request).execute_post_request():
            return Response(data=context, status=status.HTTP_200_OK)
        return Response(status=status.HTTP_400_BAD_REQUEST)


class LoginComplete(APIView):
    throttle_classes = [CustomUserRateThrottle]

    def post(self, request):
        if context := LoginCompleteService(request).execute_post_request():
            return Response(data=context, status=status.HTTP_200_OK)
        return Response(status=status.HTTP_400_BAD_REQUEST)
