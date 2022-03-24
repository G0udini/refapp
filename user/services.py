from rest_framework_simplejwt.tokens import RefreshToken

from user.crud import UserQueryset
from user.serializers import PhoneNumberSerializer, CodeSerializer
from user.utils import RedisCodeBase, MockSendSmsService, GenerateFourNumericCode


class LoginInitialService:
    def __init__(self, request):
        self.request = request
        self.serializer = PhoneNumberSerializer
        self.code_generator = GenerateFourNumericCode
        self.delivery_service = MockSendSmsService
        self.code_base = RedisCodeBase

    def _validate_and_get_data(self, serialiser):
        if serialiser.is_valid():
            return str(serialiser.validated_data["phone_number"])

    def _serialize_data(self):
        serialized_data = self.serializer(data=self.request.data)
        return self._validate_and_get_data(serialized_data)

    def execute_post_request(self):
        if phone_number := self._serialize_data():
            code = self.code_generator.gen_code()
            self.code_base.set_value(phone_number, code)
            self.delivery_service.send_mock_sms(phone_number, code)
            # Output only True here or info
            return {"Seen only in development mode": code}


class LoginCompleteService:
    def __init__(self, request):
        self.request = request
        self.serializer = CodeSerializer
        self.code_base = RedisCodeBase
        self.queryset = UserQueryset()
        self.token_service = RefreshToken

    def _validate_and_get_data(self, serialiser):
        if serialiser.is_valid():
            return (
                str(serialiser.validated_data["phone_number"]),
                serialiser.validated_data["access_code"],
            )

    def _serialize_data(self):
        serialized_data = self.serializer(data=self.request.data)
        return self._validate_and_get_data(serialized_data)

    def _validate_codes(self, phone_number, access_code):
        if base_access_code := self.code_base.get_value(phone_number):
            if base_access_code == access_code:
                self.code_base.delete_value(phone_number)
                return True

    def _get_or_create_user(self, phone_number):
        user, _ = self.queryset.get_or_create_user_by_phone(phone_number)
        return user

    def _generate_context(self, user):
        refresh = self.token_service.for_user(user)

        return {
            "refresh": str(refresh),
            "access": str(refresh.access_token),
        }

    def execute_post_request(self):
        phone_number, access_code = self._serialize_data()
        if (
            phone_number
            and access_code
            and self._validate_codes(phone_number, access_code)
        ):
            user = self._get_or_create_user(phone_number)
            return self._generate_context(user)
