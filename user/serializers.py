from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from phonenumber_field.serializerfields import PhoneNumberField
from phonenumber_field.phonenumber import to_python


class PhoneNumberFieldSerializer(PhoneNumberField):
    def to_internal_value(self, data):
        if data.startswith("8"):
            data = f"+7{data[1:]}"

        phone_number = to_python(data)
        if phone_number and not phone_number.is_valid():
            raise ValidationError(self.error_messages["invalid"])
        return phone_number


class PhoneNumberSerializer(serializers.Serializer):
    phone_number = PhoneNumberFieldSerializer()


class CodeSerializer(serializers.Serializer):
    phone_number = PhoneNumberFieldSerializer()
    access_code = serializers.CharField(max_length=4)

    def validate_access_code(self, value):
        if not value.isnumeric():
            raise ValidationError("Code is not numeric")
        return value
