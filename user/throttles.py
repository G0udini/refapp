from rest_framework.throttling import UserRateThrottle


class CustomUserRateThrottle(UserRateThrottle):
    rate = "5/minute"
