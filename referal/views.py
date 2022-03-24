from django.shortcuts import get_object_or_404
from rest_framework.generics import RetrieveAPIView
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated

from referal.services import ProfileRetrieveService
from referal.services import SubscribeToReferalService


class ProfileRetrieveView(RetrieveAPIView):
    permission_classes = [IsAuthenticated]

    def get_serializer_class(self):
        return ProfileRetrieveService.get_assotiated_serialiser(self.user_id, self.pk)

    def get_queryset(self):
        return ProfileRetrieveService().get_assotiated_queryset(self.user_id, self.pk)

    def get_object(self):
        self.pk = self.kwargs["pk"]
        self.user_id = self.request.user.id
        queryset = self.get_queryset()
        return get_object_or_404(queryset, id=self.user_id)


class SubscribeToReferalView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        return SubscribeToReferalService(
            request, kwargs.get("pk")
        ).execute_post_request()
