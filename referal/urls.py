from django.urls import path

from referal.views import ProfileRetrieveView, SubscribeToReferalView


urlpatterns = [
    path("id<int:pk>/", ProfileRetrieveView.as_view(), name="profile"),
    path("id<int:pk>/subscribe/", SubscribeToReferalView.as_view(), name="subscribe"),
]
