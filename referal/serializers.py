from django.forms import ValidationError
from django.contrib.auth import get_user_model
from rest_framework import serializers

from user.serializers import PhoneNumberFieldSerializer


class FollowersReferalSerializer(serializers.ModelSerializer):
    phone_number = PhoneNumberFieldSerializer(source="follow.phone_number")

    class Meta:
        model = get_user_model()
        fields = ("phone_number",)


class SubscribeReferalSerializer(serializers.ModelSerializer):
    referal_code = serializers.ReadOnlyField(source="own.referal_code")

    class Meta:
        model = get_user_model()
        fields = ("referal_code",)


class PublicCustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = ("phone_number", "referal_code")


class PrivateCustomUserSerializer(serializers.ModelSerializer):
    followers = FollowersReferalSerializer(source="referals", many=True)
    followed = SubscribeReferalSerializer()

    class Meta:
        model = get_user_model()
        fields = ("phone_number", "referal_code", "followed", "followers")


class SubscribeInputSerializer(serializers.Serializer):
    referal_code = serializers.CharField(max_length=6, min_length=6)

    def validate_referal_code(self, value):
        if not value.isalnum():
            raise ValidationError("Referal code is not valid")
        return value
