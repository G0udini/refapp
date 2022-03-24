from rest_framework import status
from rest_framework.response import Response

from user.crud import UserQueryset
from referal.serializers import (
    PrivateCustomUserSerializer,
    PublicCustomUserSerializer,
    SubscribeInputSerializer,
)
from referal.crud import ReferalQueryset


class ProfileRetrieveService:
    def __init__(self):
        self.queryset = UserQueryset()

    @staticmethod
    def _check_id_pk_equality(id, pk):
        return id == pk

    @classmethod
    def get_assotiated_serialiser(cls, user_id, pk):
        if cls._check_id_pk_equality(user_id, pk):
            return PrivateCustomUserSerializer
        return PublicCustomUserSerializer

    def get_assotiated_queryset(self, user_id, pk):
        if ProfileRetrieveService._check_id_pk_equality(user_id, pk):
            return self.queryset.get_user_profile()
        return self.queryset.get_all_queryset()


class SubscribeToReferalService:
    def __init__(self, request, pk):
        self.pk = pk
        self.request = request
        self.user_queryset = UserQueryset()
        self.referal_queryset = ReferalQueryset()
        self.serializer = SubscribeInputSerializer

    def _check_forbidden(self):
        return self.request.user.id != self.pk

    def _check_entered_invite_code(self):
        return self.referal_queryset.check_ref_not_exist(self.request.user)

    def _get_validated_ref_code(self):
        serializer = self.serializer(data=self.request.data)
        if serializer.is_valid():
            return serializer.validated_data.get("referal_code")

    def _check_code_with_user(self, referal_code):
        if self.request.user.referal_code == referal_code:
            return True

    def _get_referal_user(self, referal_code):
        return self.user_queryset.get_user_by_referal_code(referal_code)

    def execute_post_request(self):
        if self._check_forbidden():
            return Response(
                data={"detail": "Forbidden"}, status=status.HTTP_403_FORBIDDEN
            )

        if self._check_entered_invite_code():
            return Response(
                data={"detail": "You have already entered invite code"},
                status=status.HTTP_200_OK,
            )

        referal_code = self._get_validated_ref_code()
        if not referal_code:
            return Response(
                data={"detail": "Not valid referal code"},
                status=status.HTTP_200_OK,
            )

        if self._check_code_with_user(referal_code):
            return Response(
                data={"defatil": "You entered your referal code"},
                status=status.HTTP_200_OK,
            )

        referal_user = self._get_referal_user(referal_code)
        if not referal_user:
            return Response(
                data={
                    "detail": (
                        "User with referal code: " f"'{referal_code}', doesn't exist"
                    )
                },
                status=status.HTTP_200_OK,
            )

        self.referal_queryset.create_new_relation(referal_user, self.request.user)
        return Response(data={"detail": "Success"}, status=status.HTTP_200_OK)
