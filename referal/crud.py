from referal.models import Referal


class ReferalQueryset:
    def __init__(self):
        self.queryset = Referal.objects.all()

    def check_ref_not_exist(self, user):
        try:
            self.queryset.get(follow=user)
        except Referal.DoesNotExist:
            return False
        else:
            return True

    def create_new_relation(self, referal_user, user):
        Referal.objects.create(own=referal_user, follow=user)
