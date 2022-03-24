import redis
import time
import random
from django.conf import settings
from django.utils.crypto import get_random_string
from django.core.mail import send_mail


ACCESS_CODE_LENGTH = 4
ACCESS_ALOWED_CHARS = "0123456789"
CORPORATION_PHONE_NUMBER = "+79993330033"
CHARSET = "utf-8"


class RedisCodeBase:
    r = redis.StrictRedis(
        host=settings.REDIS_HOST,
        port=settings.REDIS_PORT,
        db=settings.REDIS_DB,
        charset=CHARSET,
        decode_responses=True,
    )

    @classmethod
    def set_value(cls, key, value, expire_time=60):
        cls.r.set(key, value, ex=expire_time)

    @classmethod
    def get_value(cls, key):
        return cls.r.get(key)

    @classmethod
    def delete_value(cls, key):
        return cls.r.delete(key)


class GenerateFourNumericCode:
    @staticmethod
    def gen_code(length=ACCESS_CODE_LENGTH, allowed=ACCESS_ALOWED_CHARS):
        return get_random_string(length=length, allowed_chars=allowed)


class MockSendSmsService:
    @staticmethod
    def send_mock_sms(phone_number, access_code, corp_phone=CORPORATION_PHONE_NUMBER):
        time.sleep(random.randint(1, 2))
        send_mail(
            "access code",
            access_code,
            corp_phone,
            [phone_number],
        )
