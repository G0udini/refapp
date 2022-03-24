from django.contrib.auth import get_user_model


class UserQueryset:
    def __init__(self):
        self.queryset = get_user_model().objects.all()

    def get_or_create_user_by_phone(self, phone_number):
        return self.queryset.get_or_create(phone_number=phone_number)

    def get_user_by_referal_code(self, referal_code):
        try:
            referal_user = self.queryset.get(referal_code=referal_code)
        except get_user_model().DoesNotExist:
            return False
        else:
            return referal_user

    def _get_user_with_followed(self):
        self.queryset = self.queryset.select_related("followed__own")

    def _get_user_with_followers(self):
        self.queryset = self.queryset.prefetch_related("referals__follow")

    def get_user_profile(self):
        self._get_user_with_followed()
        self._get_user_with_followers()
        return self.queryset

    def get_all_queryset(self):
        return self.queryset
